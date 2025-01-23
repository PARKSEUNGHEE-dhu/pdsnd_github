import time
import pandas as pd
import numpy as np

class BikeShareAnalysis:
    CITY_DATA = {
        'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv'
    }

    def __init__(self):
        self.city = None
        self.month = None
        self.day = None
        self.df = None

    def run(self):
        while True:
            self.get_filters()
            self.load_data()

            if self.df is None or len(self.df) == 0:
                print("입력하신 조건에 해당하는 데이터가 없습니다.")
            else:
                self.display_raw_data()
                self.time_stats()
                self.station_stats()
                self.trip_duration_stats()
                self.user_stats()

            restart = input("\n다시 시작하시겠습니까? 'yes' 또는 'no'를 입력하세요:\n").lower()
            if restart != 'yes':
                print("테스트를 위해 바꿉니다")
                break

    def get_filters(self):
        print("안녕하세요! 미국 자전거 데이터 분석 프로젝트에 오신것을 환영합니다.\n")

        city_names = list(self.CITY_DATA.keys())
        while True:
            city = input(f"분석할 도시시 {city_names}: ").lower()
            if city in city_names:
                self.city = city
                break

        valid_months = [
            'all', 'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
        while True:
            month = input("필터링할 월을 입력하세요 (예: 'all', 'january', ..., 'december'): ").lower()
            if month in valid_months:
                self.month = month
                break

        valid_days = [
            'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday', 'sunday'
        ]
        while True:
            day = input("필터링할 요일을 입력하세요 (예: 'all', 'monday', ..., 'sunday'): ").lower()
            if day in valid_days:
                self.day = day
                break

        print(f"\n입력된 값 - 도시: {self.city}, 월: {self.month}, 요일: {self.day}")
        print("-" * 40)

    def load_data(self):
        file_path = self.CITY_DATA[self.city]
        df_city = pd.read_csv(file_path)

        df_city["Start Time"] = pd.to_datetime(df_city["Start Time"])
        df_city["Month"] = df_city["Start Time"].dt.strftime('%B').str.lower()
        df_city["Day"] = df_city["Start Time"].dt.day_name().str.lower()

        if self.month == 'all':
            if self.day == 'all':
                self.df = df_city
            else:
                self.df = df_city[df_city["Day"] == self.day]
        else:
            if self.day == 'all':
                self.df = df_city[df_city["Month"] == self.month]
            else:
                self.df = df_city[
                    (df_city["Month"] == self.month) & (df_city["Day"] == self.day)
                ]

    def display_raw_data(self):
        start_row = 0
        end_row = 5
        while True:
            show_data = input("\n원시 데이터를 5행씩 더 보시겠습니까? 'yes' 또는 'no'로 입력하세요: ").lower()
            if show_data == 'yes':
                print(self.df.iloc[start_row:end_row])
                start_row += 5
                end_row += 5
                if start_row >= len(self.df):
                    print("\n더 이상 표시할 데이터가 없습니다.")
                    break
            elif show_data == 'no':
                print("\n원시 데이터 표시를 종료합니다.")
                break
            else:
                print("\n잘못된 입력입니다. 'yes' 또는 'no'로 입력해주세요.")

    def time_stats(self):
        print("\n가장 빈번한 여행 시간 통계를 계산 중입니다...\n")
        start_time = time.time()

        common_month = self.df["Month"].mode()[0]
        print(f"가장 흔한 월: {common_month}")

        common_day = self.df["Day"].mode()[0]
        print(f"가장 흔한 요일: {common_day}")

        self.df["Hour"] = self.df["Start Time"].dt.hour
        common_hour = self.df["Hour"].mode()[0]
        print(f"가장 흔한 시간: {common_hour}시")

        print(f"\n계산 완료 - 소요 시간: {time.time() - start_time:.4f}초")
        print("-" * 40)

    def station_stats(self):
        print("\n가장 인기 있는 출발지와 도착지, 그리고 여행 경로를 계산 중입니다...\n")
        start_time = time.time()

        common_start_station = self.df["Start Station"].mode()[0]
        print(f"가장 많이 사용된 출발지: {common_start_station}")

        common_end_station = self.df["End Station"].mode()[0]
        print(f"가장 많이 사용된 도착지: {common_end_station}")

        start_end_combo = self.df["Start Station"] + " -> " + self.df["End Station"]
        freq_combo = start_end_combo.mode()[0]
        print(f"가장 빈번한 출발지-도착지 조합: {freq_combo}")

        print(f"\n계산 완료 - 소요 시간: {time.time() - start_time:.4f}초")
        print("-" * 40)

    def trip_duration_stats(self):
        print("\n여행 시간 통계를 계산 중입니다...\n")
        start_time = time.time()

        total_travel_time = self.df["Trip Duration"].sum()
        mean_travel_time = self.df["Trip Duration"].mean()

        total_hours, total_mins, total_secs = self.get_hours_mins_secs(total_travel_time)
        mean_hours, mean_mins, mean_secs = self.get_hours_mins_secs(mean_travel_time)

        print(f"총 여행 시간: {total_hours}시간 {total_mins}분 {total_secs}초")
        print(f"평균 여행 시간: {mean_hours}시간 {mean_mins}분 {mean_secs}초")

        print(f"\n계산 완료 - 소요 시간: {time.time() - start_time:.4f}초")
        print("-" * 40)

    def get_hours_mins_secs(self, seconds):
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = round(seconds % 60, 2)
        return hours, mins, secs

    def user_stats(self):
        print("\n사용자 통계를 계산 중입니다...\n")
        start_time = time.time()

        if "User Type" in self.df.columns:
            counts_of_user_type = self.df["User Type"].value_counts()
            print("사용자 유형별 개수:")
            print("-" * 40)
            print(f"{counts_of_user_type}\n")

        if "Gender" in self.df.columns:
            counts_of_gender = self.df["Gender"].value_counts()
            print("성별별 개수:")
            print("-" * 40)
            print(f"{counts_of_gender}\n")
        else:
            print("성별 데이터가 없습니다.")

        if "Birth Year" in self.df.columns:
            oldest_year = int(self.df["Birth Year"].min())
            latest_year = int(self.df["Birth Year"].max())
            common_year = int(self.df["Birth Year"].mode()[0])
            print(f"가장 오래된 출생 연도: {oldest_year}")
            print(f"가장 최근 출생 연도: {latest_year}")
            print(f"가장 흔한 출생 연도: {common_year}")
        else:
            print("출생 연도 데이터가 없습니다.")

        print(f"\n계산 완료 - 소요 시간: {time.time() - start_time:.4f}초")
        print("-" * 40)

def main():
    analyzer = BikeShareAnalysis()
    analyzer.run()

if __name__ == "__main__":
    main()
