# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier  # 改为随机森林
from sklearn.preprocessing import LabelEncoder
import random  # 添加随机选择功能
import os
import pickle  # 用于保存和加载模型

# Define the game choices
choices = ["R", "P", "S"]
HISTORY_LENGTH = 10  # 使用过去10次选择
MODEL_PATH = "./model.pkl"  # 模型保存路径

# Encode choices to numbers
encoder = LabelEncoder()
encoder.fit(choices)

model = None
# 用于累积训练数据
training_features = []
training_labels = []

# 添加统计指标
quincy_pattern = ["R", "R", "P", "P", "S"]
abbey_counter = {"RR": 0, "RP": 0, "RS": 0, "PR": 0, "PP": 0, "PS": 0, "SR": 0, "SP": 0, "SS": 0}
abbey_last_plays = []  # 存储abbey的最近选择
abbey_detected = False  # 标记是否检测到abbey模式

def save_model(model, filename=MODEL_PATH):
    """保存训练好的模型到文件"""
    try:
        with open(filename, 'wb') as f:
            pickle.dump(model, f)
        print(f"模型已保存到 {filename}")
        return True
    except Exception as e:
        print(f"保存模型时出错: {e}")
        return False

def load_model(filename=MODEL_PATH):
    """从文件加载模型"""
    global model
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as f:
                model = pickle.load(f)
            print(f"模型已从 {filename} 加载")
            return model
        except Exception as e:
            print(f"加载模型时出错: {e}")
            return None
    else:
        print(f"模型文件 {filename} 不存在")
        return None

def get_pattern_features(opponent_history, pattern=quincy_pattern):
    """检测对手是否跟随某种固定模式"""
    if len(opponent_history) < len(pattern):
        return 0
    
    matches = 0
    for i in range(len(opponent_history) - len(pattern)):
        if opponent_history[i:i+len(pattern)] == pattern:
            matches += 1
    
    return matches / max(1, (len(opponent_history) - len(pattern)))

def get_frequency_features(opponent_history):
    """计算对手选择的频率特征"""
    if not opponent_history:
        return [1/3, 1/3, 1/3]  # 均匀分布
    
    counts = {'R': 0, 'P': 0, 'S': 0}
    for move in opponent_history:
        if move in counts:
            counts[move] += 1
    
    total = sum(counts.values())
    return [counts['R']/total, counts['P']/total, counts['S']/total]

def get_transition_features(opponent_history):
    """计算对手转换矩阵特征"""
    if len(opponent_history) < 2:
        return [1/9] * 9  # 均匀分布
    
    transitions = {
        'RR': 0, 'RP': 0, 'RS': 0,
        'PR': 0, 'PP': 0, 'PS': 0,
        'SR': 0, 'SP': 0, 'SS': 0
    }
    
    for i in range(len(opponent_history)-1):
        if opponent_history[i] in choices and opponent_history[i+1] in choices:
            key = opponent_history[i] + opponent_history[i+1]
            transitions[key] += 1
    
    # 更新全局计数器以检测abbey策略
    for key in transitions:
        if key in abbey_counter:
            abbey_counter[key] += transitions[key]
    
    total = sum(transitions.values())
    if total == 0:
        return [1/9] * 9
    
    ordered_trans = [transitions[k]/total for k in sorted(transitions.keys())]
    return ordered_trans

def get_window_stats(opponent_history, window=5):
    """获取最近窗口中的统计数据"""
    if len(opponent_history) < window:
        return [1/3, 1/3, 1/3]
    
    recent = opponent_history[-window:]
    counts = {'R': 0, 'P': 0, 'S': 0}
    for move in recent:
        if move in counts:
            counts[move] += 1
    
    total = sum(counts.values())
    return [counts['R']/total, counts['P']/total, counts['S']/total]

def create_features_from_history(history, opponent_history, window_size=HISTORY_LENGTH):
    # 如果历史记录不足10次，用'R'填充
    if len(history) < window_size:
        padding = ['R'] * (window_size - len(history))
        history = padding + history
    if len(opponent_history) < window_size:
        padding = ['R'] * (window_size - len(opponent_history))
        opponent_history = padding + opponent_history
    
    # 获取基本特征
    recent_history = history[-window_size:] + opponent_history[-window_size:]
    encoded_history = encoder.transform(recent_history)
    
    # 获取高级特征
    pattern_score = [get_pattern_features(opponent_history)]
    freq_features = get_frequency_features(opponent_history)
    trans_features = get_transition_features(opponent_history)
    recent_stats = get_window_stats(opponent_history)
    
    # 组合所有特征
    combined_features = np.concatenate([
        encoded_history,
        pattern_score,
        freq_features,
        trans_features,
        recent_stats
    ])
    
    return combined_features

def player(prev_opponent_play, history=[], opponent_history=[]):
    global model, training_features, training_labels, abbey_counter, abbey_detected

    # 首次运行时尝试加载模型
    if model is None and not training_features:
        load_model()

    if prev_opponent_play:
        opponent_history.append(prev_opponent_play)
    
    # 如果历史记录不足HISTORY_LENGTH次，返回默认选择
    if len(history) <= HISTORY_LENGTH:
        # 前几轮随机出石头剪刀布，增加多样性
        move = random.choice(choices)
        history.append(move)
        return move
    
    if prev_opponent_play:
        # 创建特征（过去10次选择 + 高级特征）
        X = create_features_from_history(history[:-1], opponent_history[:-1]) 
        # 获取对手的实际选择作为标签
        y = encoder.transform([opponent_history[-1]])[0]  # 获取单个数值
        
        # 累积训练数据
        training_features.append(X)
        training_labels.append(y)
        
        # 每累积10个新样本重新训练
        if len(training_features) % 10 == 0 or model is None:
            # 训练模型 - 使用所有累积的数据
            if model is None:
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            
            # 将列表转换为numpy数组
            X_train = np.array(training_features)
            y_train = np.array(training_labels)
            
            # 训练模型
            model.fit(X_train, y_train)
            
            # 每100轮保存一次模型
            if len(training_features) % 100 == 0:
                save_model(model)
    
    # 检测对手身份
    likely_opponent = "unknown"
    
    # 检查是否是quincy (循环模式)
    if len(opponent_history) >= 10:
        # Quincy的模式： ["R", "R", "P", "P", "S"]
        pattern_match = True
        for i in range(min(5, len(opponent_history))):
            expected = quincy_pattern[i % 5]
            if opponent_history[-5+i] != expected:
                pattern_match = False
                break
        
        if pattern_match:
            likely_opponent = "quincy"
    
    # 根据对手身份选择策略
    if likely_opponent == "quincy":
        # 对quincy的特殊处理 - 预测其固定循环
        next_index = len(opponent_history) % 5
        next_quincy_move = quincy_pattern[next_index]
        
        # 选择克制动作
        if next_quincy_move == "R":
            counter_move = "P"
        elif next_quincy_move == "P":
            counter_move = "S"
        else:  # next_quincy_move == "S"
            counter_move = "R"
            
        history.append(counter_move)
        return counter_move

    # 使用模型进行预测
    if model is not None:
        next_X = create_features_from_history(history, opponent_history)
        prediction = model.predict(next_X.reshape(1, -1))
        predicted_move = choices[prediction[0]]
        
        # 根据预测结果选择最佳应对策略
        if predicted_move == "R":
            counter_move = "P"
        elif predicted_move == "P":
            counter_move = "S"
        else:  # predicted_move == "S"
            counter_move = "R"
        
        history.append(counter_move)
        return counter_move
    else:
        # 如果模型尚未训练，使用最近的统计
        stats = get_window_stats(opponent_history)
        max_idx = np.argmax(stats)
        
        if max_idx == 0:  # R最多
            counter_move = "P"
        elif max_idx == 1:  # P最多
            counter_move = "S"
        else:  # S最多
            counter_move = "R"
        
        history.append(counter_move)
        return counter_move

# 读取数据文件
def parse_game_data(filename):
    data = {"Player": [], "Bot": []}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if line.startswith('Player 1:'):
            # 解析玩家的选择
            parts = line.split('|')
            p1_move = parts[0].split(':')[1].strip()
            p2_move = parts[1].split(':')[1].strip()
            if p1_move in choices and p2_move in choices:
                data['Player'].append(p1_move)
                data['Bot'].append(p2_move)
            
    return pd.DataFrame(data)

def create_sequence_features(df, window_size=HISTORY_LENGTH):
    """创建序列特征"""
    sequences = []
    labels = []
    
    player = df['Player'].tolist()
    bot = df['Bot'].tolist()
    
    for i in range(len(player) - window_size - 1):
        # 基本特征
        player_seq = player[i:i + window_size]
        bot_seq = bot[i:i + window_size]
        sequence = player_seq + bot_seq
        
        # 添加高级特征
        pattern_score = [get_pattern_features(bot_seq[:i+window_size])]
        freq_features = get_frequency_features(bot_seq[:i+window_size])
        trans_features = get_transition_features(bot_seq[:i+window_size])
        recent_stats = get_window_stats(bot_seq[:i+window_size])
        
        # 编码序列特征
        encoded_sequence = encoder.transform(sequence)
        
        # 组合所有特征
        combined_features = np.concatenate([
            encoded_sequence,
            pattern_score,
            freq_features,
            trans_features,
            recent_stats
        ])
        
        sequences.append(combined_features)
        # 使用机器人的下一步作为标签
        labels.append(bot[i+window_size+1])
    
    X = np.array(sequences)
    y = encoder.transform(labels)
    
    return X, y

def train_model(data):
    """从数据训练一个新模型并保存"""
    if len(data["Player"]) <= HISTORY_LENGTH:  # 需要超过窗口大小的数据才能训练
        return None
        
    df = pd.DataFrame(data)
    X, y = create_sequence_features(df)
    
    if len(X) == 0:  # 如果没有足够的序列
        return None
        
    trained_model = RandomForestClassifier(n_estimators=100, random_state=42)
    trained_model.fit(X, y)
    
    # 保存训练好的模型
    save_model(trained_model)
    
    return trained_model

def predict_move(model, history, opponent_history):
    if model is None or len(history) < HISTORY_LENGTH:
        return "R"
        
    X = create_features_from_history(history, opponent_history)
    prediction = model.predict(X.reshape(1, -1))
    predicted_move = choices[prediction[0]]
    
    # 返回克制预测动作的动作
    if predicted_move == "R":
        return "P"
    elif predicted_move == "P":
        return "S"
    else:  # predicted_move == "S"
        return "R"