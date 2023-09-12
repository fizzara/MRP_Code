import os
for i in range(1, 12):
    os.system(f"tesseract eng.undertale.exp{i}.png eng.undertale.exp{i} --psm 6 nobatch box.train")