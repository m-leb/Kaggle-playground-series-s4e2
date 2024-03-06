# Kaggle - Playground Series
##### Season 4, Episode 2
### Multi-Class Prediction of Obesity Risk

В рамках этого учебного соревнования, на основании анкетных данных пользователей, сгенерированных нейронной сетью обученной на оригинальном датасете [Obesity or CVD risk](https://www.kaggle.com/datasets/aravindpcoder/obesity-or-cvd-risk-classifyregressorcluster), необходимо было предсказать уровень ожирения. Оценка качества по accuracy.

## Моя финальная модель на Privat имела точность: **0.90597**.

От лидера я отстал на **0.0056**. Его точность составила **0.91157**. Будем честны, для данного учебного датасета такая разница была существенной, моя точность была представлена в **топ 33%**. При этом, разница между точностью public и privat оказалась в **1024 мест**, что говорит о хорошей обобающей способности моей модели, по сравнению со многоими другими, которые изначально находились выше меня.

[1. EDA](#EDA)

[2. Base model](#BASE)

[3. Анализ ошибок и выбор архитектуры](#variance)

[4. Fine tuning](#finetuning)

[5. Заключение](#end)

---

## <a id="EDA">EDA</a>

Подробно EDA представлен в ноутбуке проекта: **EDA.ipynb**

В целом, так как данные сгенерированы, они были довольно чистыми, с точки зрения отсутствующих значений. Далеко не все, но часть признаков были распределены равномерно, что сохраняло логику. Стало очевидным, что рост и вес сильно коррелируют между собой, а также с таргетом. Логично было сделать из них признак BMI, который, насколько я понимаю, является основой для вывода об уровне ожирения. В последствии было очевидно, что хотя BMI был наиболее информативным признаком, его не хватало для достижения хорошей точности.

---

## <a id="BASE">Базовая модель</a>

Обучение базовой модели представлено в ноутбуке проекта: **base_model.ipynb**

Было опробовано несколько простых (с точки зрения затраты времени) моделей. Я пробовал рассмотреть эту задачу, как задачу регресси, так как таргет - ранговый. Пробовал различные подходы к мультиклассовым задачам. В итоге, что не удивительно, градиентный бустинг дал наилучший результат. Без подбора параметров и особой работы с признаками на валидации точность составила **0.88367**. Точность на public **0.88186**. От этого решил и отталкиваться.

---

## <a id="variance">Анализ ошибок и выбор архитектуры</a>

Далее начал эксперементировать с архитектурой. Эксперементы представлены в ноутбуках: model1.ipynb, model+optuna.ipynb, poly.ipynb. В дальнейшем, будет замечено, что кроме создания нового признака BMI, можно было ещё поработать с признаками. Но, что касается, например, выбросов, я не стал обрабатывать модель руководствуясь тем, что раз сами данные сгенерированы нейросетью, то мне стоит обучать модель на всех данных, так как в тесте вероятно данные будут распределены также. С одной стороны, моя финальная модель имела хорошую обобщающую способность и возможно оставлять выбросы было оправдано, но с другой, как оказалось, тестовые данные стоило рассмотреть подробнее, об этом в заключении.

### model1.ipynb

Начал я с того, что более подробно рассмотрел как предсказывает базовая модель различные классы, чтобы оценить на каком классе можель ошибается больше. Здесь же радилась идея, которая частично дожидала до финала - объеденить рядом стоящие (по рангу) классы в группы. Определять сначала такую группу, а уже потом отдельно внутри группы строить предсказание класса. Сильного быста не было.

### model+optuna.ipynb

Здесь я решил развить текущую идею с ансамблем моделей. Модель предсказывала классы (где высокая точность) и группы классов (где точность ниже), дальше, отдельные модели обученные на таких группах предсказывали конкретный класс. Кроме того, я сразу решил посмотреть, какой максимум можно выжать из такого подхода, поэтому полученные модели зафайнтюнил с помощью библиотеки optuna и в итоге на public получил точность **0.89342**, что немного выше базового результата. Но результат все-таки скорее неудовлетворительный.

### poly.ipynb

Поэтому возникла мысль посмотреть различные полиномиальные сочетания признаков. Перебрав несколько вариантов, на валидации модель обученная без добавления других признаков показывала себя немного лучше, поэтому добавлять ничего не стал из-за страха зашумить модель, так как, конечно, наиболее значимыми были признаки так или иначе касающиеся BMI или роста и веса, а из этого признака и так извлекается достаточно информации и хочется, чтобы модель не забывала про другие. Но, при дальнейшем анализе чужих работ, заметил очень разумную вещь. На ряду с BMI там были признаки сочетающиеся по смыслу, например частота потребления высококалорийной пищи и количество приемом пищи и т.п. Соответственно из них можно было сделать смысловые признаки, например, частота употребления калорийной пищи в единицу приема или количество активности и передвижение. В общем, сгруппировать признаки и выделить из них те, которые можно постараться привести к единичному значению, где есть советание значения и частоты.

---

## <a id="EfinetuningDA">Fine tuning</a>

В своей последней попытке (poly.ipynb) я обратил внимание на те классы в которых моя модель ошибалась наиболее часто. А самое главное, сравнил это с теми предсказаниями, которые она дает. Это наложилось на недавно просмотренное выступление команды Яндекса на [Data Dojo. ML тренировки](https://www.youtube.com/watch?v=V9omCycXcRc) откуда отчетливо вспомнился тезис: если модель не должна работать быстро, значит стоит пробовать ансамбли.

Выбрав в итоге проблемные группы, я обучил множество моделей. После чего, из каждой модели я собрал предсказания в один датасет и обучил модель на предсказаниях всех этих моделей.

Обучение финальной модели представлено в ноутбуке: **final.ipynb**

Были обучены следующие градиентные бустинги на всех признаках с добавлением BMI:

- Мультиклассовая модель на всех классах
- Бинарная классификация: ожирение или нет
- Бинарная классификация: овервейт или нет
- Бинарная классификация: нормальный/недовес или нет
- Бинарная классификация: нормальный вес или недовес
- Бинарная классификация: нормальный вес или перевес тип 1
- Бинарная классификация: перевес тип 1 или тип 2
- Бинарная классификация: ожирение тип 1 или тип 2

Бинарная классификация по определению конкретного значения (последние 4 модели) были обучены, конечно, только на тех объектах, где было то или иное значение, но применялись потом для всех. Идея была в том, что эти признаки долны помочь определиться в случаях неопределенности и не учитываться, когда финальной модели ясно куда отнести объект.

Финальная модель строилась на признаках представленных как вероятность принадлежности к классу. Из предсказаний каждой модели была выкинута одна колонка, чтобы не нагружать модель лишними вычислениями, так как эти данные избыточны.

По хорошему, для адекватной оценки такой "двухступенчатой модели" необходимо делить начальную выборку на три группы. Трейн, тест и валидация, так как при делении только на две: мы учимыся и валидируемся на первом этапе. Дальше, когда мы будем учиться на третьем этапе, мы будем иметь дело с моделями, на которых уже валидировались, а значит некоторая утечка информации от них была и валидироваться снова на этих же данных не совсем корректно.

Но так как это соревнование, в качестве винального валидационного датасета я рассматривал public test и принял решение игнорировать описанное выше предостережение. Ещё и в связи с амлом временем до окончания контеста.

Кроме того, влияние валидации на первом этапе было не таким существенным, потому что в связи с малым временем также было принято файнтюнить только на втором этапе, а значит эта проблема не должна сильно повлиять на обобщающую способность модели.

С помощью этого подхода было сделано два предсказания. Без файнтюнинга и с файнтюнингом с помощью optuna.

| Финальная модель | Public Score | Privat Score |
| ---------------- | ------------ | ------------ |
| Без файнтюнинга  | 0.90462      | 0.90417      |
| С файнтюнингом   | 0.90462      | 0.90597      |

---

## <a id="end">Заключение</a>

Опыт этого соревнования научил меня следующему:

Конечно, соревновательное МЛ отличается от того, в котором я практиковался раньше. Здесь меньше стеснения для брутфорс решений, так как борба идет за каждую десятитысячную. Но и переусердствовать с этим нельзя. Почти весь топ на public улетел вниз.

#### Стоит рассматривать признаки не только трейна, но и теста

Как я говорил выше, тестовые данные стоило рассмотреть подробнее. Так как это мой первый опыт участия в свободном соревновании (до этого участвовал только в соревнованиях в рамках различных курсов, например от Deep Learning School), я решил что тестовые данные не имеют такой высокой значимости и нужно сосредоточиться на трейне и архитектуре.

В последствии оказалось, что, как минимум в паблике, у одного из категориальных признаков было другое распределение, а именно, в тесте одного из вариантов ответа просто не было. Не знаю насколько это было значимо, но если бы я обратил на это внимание, я бы обязательно это проверил, и, как вариант, в принципе исключил бы этот признак.

#### Больше уделить внимание содержанию признаков и их смыслу

Выше в описании попытки полиномиального создания новых признаков, я это уже описал. Используемый мной полиномиальный подход использовал степени > 1, в связи с чем не было рассмотрено вариантов деления признака одного на другой. Возможно, это могло бы дать какой-то полезный признак. Тдея эта могла бы прийти, если бы я больше внимания дулели смыслу признаков. Создание BMI лежало на поверхности, но предположение, что значение признакака можно связать с частотой его проявления - тоже было недалеко.
