import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Настройка стиля и шрифта (для поддержки кириллицы)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12

# Создание данных
n = np.linspace(1, 100, 1000)  # Число процессоров от 1 до 100

# Формулы ускорения
# Амдал: S = 1 / (f + (1 - f)/n), где f - доля последовательной части
f_amdahl = 0.1  # 10% последовательной части
S_amdahl = 1 / (f_amdahl + (1 - f_amdahl)/n)

# Густафсон: S = n + f*(1 - n), где f - доля последовательной части
f_gustafson = 0.1  # 10% последовательной части
S_gustafson = n + f_gustafson*(1 - n)

# Сана-Ная (Sun-Ni): S = (1 - f + f*n) / (1 - f + f*n^(1/3))
# Это упрощенная модель для демонстрации
f_sun_ni = 0.1  # 10% последовательной части
S_sun_ni = (1 - f_sun_ni + f_sun_ni*n) / (1 - f_sun_ni + f_sun_ni*np.power(n, 1/3))

# Создание графика
fig, ax = plt.subplots(figsize=(10, 7))

# Построение кривых
ax.plot(n, S_amdahl, 'b-', linewidth=2, label='Амдал')
ax.plot(n, S_gustafson, 'r-', linewidth=2, label='Густафсон')
ax.plot(n, S_sun_ni, 'g-', linewidth=2, label='Сана-Ная')

# Настройка осей
ax.set_xlabel('Число процессоров (n)', fontsize=14)
ax.set_ylabel('Ускорение (S(n))', fontsize=14)
ax.set_title('Зависимость ускорения от числа процессоров', fontsize=16)

# Логарифмические шкалы
ax.set_xscale('log')
ax.set_yscale('log')

# Установка пределов осей
ax.set_xlim(1, 100)
ax.set_ylim(1, 1000)

# Настройка сетки
ax.grid(True, which='both', alpha=0.3)
ax.grid(True, which='major', alpha=0.6)

# Настройка делений на осях
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

# Добавление легенды
ax.legend(loc='upper left', fontsize=12)

# Добавление аннотаций
ax.text(50, 10, 'Амдал', color='blue', fontsize=11, ha='center')
ax.text(50, 200, 'Густафсон', color='red', fontsize=11, ha='center')
ax.text(20, 80, 'Сана-Ная', color='green', fontsize=11, ha='center')

# Отображение графика
plt.tight_layout()
plt.show()

# Для сохранения в файл
# plt.savefig('ускорение_процессоров.png', dpi=300, bbox_inches='tight')