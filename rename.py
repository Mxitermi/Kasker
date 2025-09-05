import os
import shutil

# Pfade anpassen
source_folder = r'C:\data\python\CineTrack\Samples\Masks'
target_folder = os.path.join(source_folder, 'restored')

# Zielordner erstellen, wenn er nicht existiert
os.makedirs(target_folder, exist_ok=True)

# Mapping: Aktueller Name (.png) → Ursprünglicher Name (.png)
reverse_mapping = {
    '0.png': '0.png',
    '1.png': '1.png',
    '2.png': '10.png',
    '3.png': '12.png',
    '4.png': '15.png',
    '5.png': '19.png',
    '6.png': '2.png',
    '7.png': '24.png',
    '8.png': '25.png',
    '9.png': '26.png',
    '10.png': '27.png',
    '11.png': '28.png',
    '12.png': '29.png',
    '13.png': '3.png',
    '14.png': '30.png',
    '15.png': '31.png',
    '16.png': '32.png',
    '17.png': '33.png',
    '18.png': '34.png',
    '19.png': '35.png',
    '20.png': '36.png',
    '21.png': '37.png',
    '22.png': '38.png',
    '23.png': '39.png',
    '24.png': '4.png',
    '25.png': '40.png',
    '26.png': '41.png',
    '27.png': '42.png',
    '28.png': '43.png',
    '29.png': '44.png',
    '30.png': '45.png',
    '31.png': '46.png',
    '32.png': '47.png',
    '33.png': '48.png',
    '34.png': '49.png',
    '35.png': '50.png',
    '36.png': '51.png',
    '37.png': '52.png',
    '38.png': '53.png',
    '39.png': '54.png',
    '40.png': '55.png',
    '41.png': '56.png',
    '42.png': '57.png',
    '43.png': '58.png',
    '44.png': '59.png',
    '45.png': '60.png',
    '46.png': '61.png',
    '47.png': '62.png',
    '48.png': '67.png',
    '49.png': '70.png',
    '50.png': '71.png',
    '51.png': '72.png',
    '52.png': '73.png',
    '53.png': '74.png',
    '54.png': '75.png',
    '55.png': '76.png',
    '56.png': '77.png',
    '57.png': '78.png',
    '58.png': '79.png',
    '59.png': '8.png',
    '60.png': '80.png',
    '61.png': '81.png',
    '62.png': '82.png',
    '63.png': '83.png',
    '64.png': '84.png',
    '65.png': '85.png',
    '66.png': '86.png',
    '67.png': '87.png',
    '68.png': '89.png',
    '69.png': '9.png',
    '70.png': '90.png',
    '71.png': '91.png',
    '72.png': '92.png',
    '73.png': '93.png',
    '74.png': '94.png',
    '75.png': '95.png'
}

copied = 0
skipped = 0

for current, original in reverse_mapping.items():
    source_path = os.path.join(source_folder, current)
    target_path = os.path.join(target_folder, original)

    if os.path.exists(source_path):
        shutil.copy2(source_path, target_path)
        print(f"Copied & renamed: '{current}' → '{original}'")
        copied += 1
    else:
        print(f"Skipped missing file: '{current}'")
        skipped += 1