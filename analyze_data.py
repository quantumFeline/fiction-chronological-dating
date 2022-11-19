import json
import matplotlib.pyplot as plt

files = ["data.json", "data2.json"]
CURRENT_YEAR = 2022

if __name__ == "__main__":
    years = [0]*(CURRENT_YEAR+1)

    for filename in files:
        with open(filename, "rb") as file:
            data = json.load(file)
            for title in data:
                years[int(title["year"])] += 1
    print(years)
    print(sum(years))
    plt.plot(years)
    plt.xlim([1800, 1950])
    plt.show()
