from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

logos_folder = 'static/logos'
team_logos = {}
# Lặp qua các tệp trong thư mục logo
for filename in os.listdir(logos_folder):

    team_name = os.path.splitext(filename)[0]

    logo_path = os.path.join(logos_folder, filename).replace('\\','/')

    team_logos[team_name] = logo_path

# Load model từ file
loaded_model = joblib.load('\model\L5M\best_random_forest_L5M.joblib')

# Load dữ liệu cần thiết
home_l5m = pd.read_csv('dulieududoan/dudoan_home.csv')
away_l5m = pd.read_csv('dulieududoan/dudoan_away.csv')

# Mã hóa tên đội thành số
home_l5m['HomeTeam_code'] = home_l5m['HomeTeam'].astype('category').cat.codes
away_l5m['AwayTeam_code'] = away_l5m['AwayTeam'].astype('category').cat.codes

# Tạo dictionary để map tên đội với mã số
home_team_dict = dict(zip(home_l5m['HomeTeam'], home_l5m['HomeTeam_code']))
away_team_dict = dict(zip(away_l5m['AwayTeam'], away_l5m['AwayTeam_code']))

@app.route('/')
def home():
    teams = home_l5m['HomeTeam'].unique()
    return render_template('index.html', teams=teams)

@app.route('/underway')
def underway():
    teams = home_l5m['HomeTeam'].unique()
    return render_template('underway.html', teams=teams)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    home_team = data.get('hometeam')
    away_team = data.get('awayteam')

    if home_team == away_team:
        return jsonify({'error': 'Home team and away team cannot be the same.'})

    try:
        # Lấy mã số của đội nhà và đội khách
        home_team_code = home_team_dict[home_team]
        away_team_code = away_team_dict[away_team]

        # Lấy thông tin đội nhà và đội khách dựa trên mã số
        home_info = home_l5m[home_l5m['HomeTeam_code'] == home_team_code].iloc[0]
        away_info = away_l5m[away_l5m['AwayTeam_code'] == away_team_code].iloc[0]

        # Tạo dataframe đầu vào cho model
        input_data = pd.DataFrame({
            'HomeTeam': [home_info['HomeTeam_code']],
            'AwayTeam': [away_info['AwayTeam_code']],
            'AC_away': [away_info['AC_away']],
            'AF_away': [away_info['AF_away']],
            'AR_away': [away_info['AR_away']],
            'AS_away': [away_info['AS_away']],
            'AST_away': [away_info['AST_away']],
            'AY_away': [away_info['AY_away']],
            'FTAG_away': [away_info['FTAG_away']],
            'FTHG_home': [home_info['FTHG_home']],
            'HC_home': [home_info['HC_home']],
            'HF_home': [home_info['HF_home']],
            'HR_home': [home_info['HR_home']],
            'HS_home': [home_info['HS_home']],
            'HST_home': [home_info['HST_home']],
            'HY_home': [home_info['HY_home']],
            'LSHW_home': [home_info['LSHW_home']],
            'LSHD_home': [home_info['LSHD_home']],
            'LSAW_away': [away_info['LSAW_away']],
            'LSAD_away': [away_info['LSAD_away']]
        })

        desired_order = [
            'HomeTeam', 'AwayTeam','LSHW_home','LSAW_away','LSHD_home','LSAD_away','FTHG_home','FTAG_away','HC_home','AC_away','HF_home',
            'AF_away','HR_home','AR_away', 'HS_home','AS_away', 'HST_home', 'AST_away','HY_home','AY_away'
        ]

        # Sắp xếp lại các cột theo thứ tự mong muốn
        input_data = input_data.reindex(columns=desired_order)

        # Dự đoán kết quả
        prediction = loaded_model.predict(input_data)

        # In kết quả
        result = ""
        logo_path = ""
        if prediction[0] == 2:
            result =  f"{home_team} Winners"
            logo_path = team_logos[home_team]
        elif prediction[0] == 0:
            result = f"{away_team} Winners"
            logo_path = team_logos[away_team]
        else:
            logo_path = 'static/logos/hoa.png'
            result = "hòa"
        
        return jsonify({'prediction': result, 'logo': logo_path})

    except KeyError as e:
        return jsonify({'error': 'Invalid team name provided.'})
    
# Load pre-trained model
model = joblib.load('model/rf_model.pkl')

# API endpoint for prediction
@app.route('/predict/underaway', methods=['POST'])
def predict_underway():
    data = request.json
    home_team = data.get('hometeam')
    away_team = data.get('awayteam')

    if home_team == away_team:
        return jsonify({'error': 'Home team and away team cannot be the same.'})

    try:
                # Lấy mã số của đội nhà và đội khách
        home_team_code = home_team_dict[home_team]
        away_team_code = away_team_dict[away_team]

        # Lấy thông tin đội nhà và đội khách dựa trên mã số
        home_ud = home_l5m[home_l5m['HomeTeam_code'] == home_team_code].iloc[0]
        away_ud = away_l5m[away_l5m['AwayTeam_code'] == away_team_code].iloc[0]  

        # Preprocess data
        try:
            ht_home = float(data['ht_home'])
            ht_away = float(data['ht_away'])
            ft_home = float(data['ft_home'])
            ft_away = float(data['ft_away'])
            hs = float(data['hs'])
            as_ = float(data['as'])
            hst = float(data['hst'])
            ast = float(data['ast'])
            hc = float(data['hc'])
            ac = float(data['ac'])
            hf = float(data['hf'])
            af = float(data['af'])
            hy = float(data['hy'])
            ay = float(data['ay'])
            hr = float(data['hr'])
            ar = float(data['ar'])
        except ValueError:
            return jsonify({'error': 'Please enter enough parameters to make a prediction!'})

        # Make prediction
        prediction = model.predict([[ht_home, ht_away, ft_home, ft_away, hs, as_, hst, ast, hc, ac, hf, af, hy, ay, hr, ar]])
        result = ""
        logo_path = ""
        # Prepare response
        if prediction[0] == 1:
            result =  f"{home_team} Winners"
            logo_path = team_logos[home_team]
        elif prediction[0] == -1:
            result = f"{away_team} Winners"
            logo_path = team_logos[away_team]
        else:
            logo_path = 'static/logos/hoa.png'
            result = "hòa"
        
        return jsonify({'prediction': result, 'logo': logo_path})
    except Exception as e:
        # Handle errors
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 400

    
@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

if __name__ == '__main__':
    app.run(debug=True)
