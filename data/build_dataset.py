import pandas as pd
import random

num_students = 10000

# Xd ket qua dua tren tieu chi
def determine_results(tinhtrangkinhte, gpa, songayvang, lamthem, tinhtrangsuckhoe):
    
    if songayvang >= 6:  
        return 0
    elif songayvang >= 3:
        base_chance = 0.075
    else:
        base_chance = 0

    if gpa < 1.0:
        return 0
    elif gpa < 2.0:
        base_chance += 0.1
    elif gpa < 2.5: 
        base_chance += 0.05
    elif gpa < 3.0:
        base_chance += 0
    elif gpa < 3.5:
        base_chance -= 0.2
    else:
        return 1

    if tinhtrangkinhte == "Hộ nghèo":
        base_chance += 0.05
    elif tinhtrangkinhte == "Hộ cận nghèo":
        base_chance += 0.025
    elif tinhtrangkinhte == "Bình thường":
        base_chance -= 0.1
    elif tinhtrangkinhte == "Giàu":
        base_chance += 0.025
    
    if lamthem == 1:
        base_chance += 0.025
    
    if tinhtrangsuckhoe == "Bị bệnh":
        base_chance += 0.1

    # Giới hạn xs
    base_chance = min(base_chance, 1.0)

    return 0 if random.random() < base_chance else 1
    
def generate_gpa():
    if random.random() < 0.4:
        return round(random.uniform(0, 2.5), 2)
    else:
        return round(random.uniform(2.5, 4.0), 2)

def generate_songayvang():
    if random.random() < 0.1:
        return round(random.uniform(4, 15))
    else:
        return round(random.uniform(0, 3))

# tao dataset
data = []
for i in range(1, num_students+1):
    tuoi = random.randint(18,23)
    gioitinh = random.choice(["Nam", "Nữ"])
    tinhhinhkinhte = random.choices(
        ["Hộ nghèo", "Hộ cận nghèo", "Bình thường", "Giàu"],
        weights=[10, 10, 60, 20]
    )[0]
    gpa = generate_gpa()
    sotinchihoanthanh = random.randint(20, 120)
    songayvang = generate_songayvang()
    lamthem = random.choice([0, 1])
    tinhhinhsuckhoe = random.choices(
        ["Bình thường", "Bị bệnh"],
        weights=[98, 2]
    )[0]
    ketqua = determine_results(tinhhinhkinhte, gpa, songayvang, lamthem, tinhhinhsuckhoe)

    data.append([
        f"IT{i}", tuoi, gioitinh, tinhhinhkinhte, gpa, sotinchihoanthanh, 
        songayvang, lamthem, tinhhinhsuckhoe, ketqua
    ])

# tao dataframe
columns = [
    "Mã SV", "Tuổi", "Giới tính", "Tình hình kinh tế", "GPA", 
    "Số tín chỉ hoàn thành", "Số ngày vắng (Không phép)", "Làm thêm",
    "Tình hình sức khỏe", "Kết quả"
]

df = pd.DataFrame(data, columns=columns)

# Xuat excel
output_file = "students_dataset.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"File da dc tao: {output_file}")


