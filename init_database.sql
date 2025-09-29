-- Создание базы данных и таблиц для Telegram Mini App
-- Индекс Личностной Реализации (ИЛР)
-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen_at TIMESTAMP WITH TIME ZONE,
    last_test_at TIMESTAMP WITH TIME ZONE
);
-- Создание таблицы результатов тестирования
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    taken_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_score INTEGER NOT NULL,
    happiness_score INTEGER NOT NULL,
    selfreal_score INTEGER NOT NULL,
    freedom_score INTEGER NOT NULL,
    happiness_pct DECIMAL(5, 2) NOT NULL,
    selfreal_pct DECIMAL(5, 2) NOT NULL,
    freedom_pct DECIMAL(5, 2) NOT NULL,
    version TEXT NOT NULL DEFAULT 'v1',
    meta JSONB
);
-- Создание таблицы вопросов
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    number INTEGER UNIQUE NOT NULL,
    text TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('happiness', 'selfreal', 'freedom')),
    max_points INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Создание таблицы вариантов ответов
CREATE TABLE IF NOT EXISTS question_options (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    points INTEGER NOT NULL,
    sort_index INTEGER NOT NULL
);
-- Создание индексов для оптимизации
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_results_user_id ON results(user_id);
CREATE INDEX IF NOT EXISTS idx_results_taken_at ON results(taken_at);
CREATE INDEX IF NOT EXISTS idx_questions_number ON questions(number);
CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category);
CREATE INDEX IF NOT EXISTS idx_question_options_question_id ON question_options(question_id);
-- Очистка таблиц перед заполнением
TRUNCATE TABLE question_options CASCADE;
TRUNCATE TABLE questions CASCADE;
-- Заполнение таблицы вопросов
-- Категория "Счастье" (вопросы 1-36, макс. 42 балла)
INSERT INTO questions (number, text, category, max_points)
VALUES (
        1,
        'Проходили полный Чек-Ап здоровья ТБН за последние 2 года?',
        'happiness',
        2
    ),
    (
        2,
        'Вылечили все свои заболевания из Чек-Апа здоровья ТБН?',
        'happiness',
        3
    ),
    (
        3,
        'Делаете силовые тренировки стабильно 2-3 раза в неделю?',
        'happiness',
        1
    ),
    (
        4,
        'Делаете кардио-тренировки стабильно 2-3 раза в неделю?',
        'happiness',
        1
    ),
    (
        5,
        'Делаете растяжку 2-3 раза в неделю?',
        'happiness',
        1
    ),
    (
        6,
        'Занимаетесь активными видами спорта не менее 1 раза в неделю?',
        'happiness',
        1
    ),
    (
        7,
        'Занимаетесь спортом более 3 раз в неделю?',
        'happiness',
        1
    ),
    (
        8,
        'Питаетесь правильно на ежедневной основе, учитывая индивидуальные особенности вашего ЖКТ?',
        'happiness',
        1
    ),
    (
        9,
        'Исключили неправильное питание из своего рациона?',
        'happiness',
        1
    ),
    (
        10,
        'Пьете достаточное количество воды в день в зависимости от ваших особенностей организма и массы тела?',
        'happiness',
        1
    ),
    (
        11,
        'Принимаете БАДы в соответствии с нехваткой микроэлементов?',
        'happiness',
        1
    ),
    (12, 'Не едите за 3 часа до сна?', 'happiness', 1),
    (
        13,
        'Исключили алкоголь из своей жизни?',
        'happiness',
        1
    ),
    (
        14,
        'Исключили курение из своей жизни?',
        'happiness',
        1
    ),
    (
        15,
        'Ложитесь спать в соответствии с Вашими циркадными ритмами?',
        'happiness',
        1
    ),
    (
        16,
        'Минимизируете и контролируете стрессовые ситуации?',
        'happiness',
        2
    ),
    (
        17,
        'Соответствуют ли показатели вашего тела норме (Уровень жира < 22%, ИМТ < 25)?',
        'happiness',
        1
    ),
    (18, 'Здоровая ли у вас кожа?', 'happiness', 1),
    (19, 'Ухаживаете ли вы за собой?', 'happiness', 1),
    (
        20,
        'Довольны ли вы своим стилем?',
        'happiness',
        1
    ),
    (
        21,
        'Работаете ли вы над своим личным развитием?',
        'happiness',
        1
    ),
    (
        22,
        'Работаете ли вы над своим профессиональным ростом?',
        'happiness',
        1
    ),
    (
        23,
        'Проводите активно и разнообразно свой досуг?',
        'happiness',
        1
    ),
    (
        24,
        'Читаете классическую литературу?',
        'happiness',
        1
    ),
    (
        25,
        'Читаете профессиональную литературу?',
        'happiness',
        1
    ),
    (
        26,
        'Путешествуете на лежачий отдых?',
        'happiness',
        1
    ),
    (
        27,
        'Путешествуете на спортивный отдых?',
        'happiness',
        1
    ),
    (
        28,
        'Путешествуете в трипы по городам?',
        'happiness',
        1
    ),
    (29, 'Ходите в экспедиции?', 'happiness', 1),
    (
        30,
        'Отдыхаете 4 и более раза в году?',
        'happiness',
        1
    ),
    (31, 'Есть ли у вас отношения?', 'happiness', 2),
    (
        32,
        'Здоровые ли у вас отношения?',
        'happiness',
        2
    ),
    (
        33,
        'Поддерживаете отношения с семьей (родители, родственники)?',
        'happiness',
        1
    ),
    (
        34,
        'Здоровые ли у вас отношения с семьей?',
        'happiness',
        1
    ),
    (
        35,
        'Поддерживаете отношения с друзьями?',
        'happiness',
        1
    ),
    (
        36,
        'Здоровые ли у вас отношения с друзьями?',
        'happiness',
        1
    );
-- Категория "Самореализация" (вопросы 37-46, макс. 48 баллов)
INSERT INTO questions (number, text, category, max_points)
VALUES (37, 'Работаете в найме?', 'selfreal', 1),
    (
        38,
        'Удовлетворены своей работой в найме?',
        'selfreal',
        1
    ),
    (
        39,
        'Работаете/Подрабатываете на себя?',
        'selfreal',
        1
    ),
    (
        40,
        'Удовлетворены своей работой/подработкой на себя?',
        'selfreal',
        1
    ),
    (
        41,
        'Являетесь учредителем/соучредителем в бизнесе?',
        'selfreal',
        2
    ),
    (
        42,
        'Удовлетворены своей работой в бизнесе?',
        'selfreal',
        2
    ),
    (
        43,
        'Уровень вашего инвестиционного капитала на текущий момент:',
        'selfreal',
        10
    ),
    (
        44,
        'Уровень окружения, с которым вы общаетесь:',
        'selfreal',
        10
    ),
    (
        45,
        'Ваш текущий уровень активных доходов:',
        'selfreal',
        10
    ),
    (
        46,
        'Ваш текущий уровень пассивных доходов:',
        'selfreal',
        10
    );
-- Категория "Свобода" (вопросы 47-51, макс. 10 баллов)
INSERT INTO questions (number, text, category, max_points)
VALUES (
        47,
        'Живете в стране/странах, в которой/которых хотите?',
        'freedom',
        2
    ),
    (
        48,
        'Живете в городе/городах, в котором/которых хотите?',
        'freedom',
        2
    ),
    (
        49,
        'Есть собственная квартира в городе/городах, где хотите жить?',
        'freedom',
        2
    ),
    (
        50,
        'Есть собственная машина в городе/городах, где хотите жить?',
        'freedom',
        2
    ),
    (
        51,
        'Чувствуете себя ментально свободными?',
        'freedom',
        2
    );
--
Заполнение вариантов ответов для вопросов категории "Счастье" -- Вопрос 1: Проходили полный Чек-Ап здоровья ТБН за последние 2 года?
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 1
        ),
        'Да',
        2,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 1
        ),
        'Не полн',
        1,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 1
        ),
        'Нет',
        0,
        3
    );
-- Вопрос 2: Вылечили все свои заболевания из Чек-Апа здоровья ТБН?
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 2
        ),
        'Да',
        3,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 2
        ),
        'Не полн',
        1,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 2
        ),
        'Нет',
        0,
        3
    );
-- Вопросы 3-15: Да/Нет (1 балл за "Да")
INSERT INTO question_options (question_id, label, points, sort_index)
SELECT q.id,
    'Да',
    1,
    1
FROM questions q
WHERE q.number BETWEEN 3 AND 15
UNION ALL
SELECT q.id,
    'Нет',
    0,
    2
FROM questions q
WHERE q.number BETWEEN 3 AND 15;
-- Вопрос 16: Минимизируете и контролируете стрессовые ситуации?
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 16
        ),
        'Да',
        2,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 16
        ),
        'Не полн',
        1,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 16
        ),
        'Нет',
        0,
        3
    );
-- Вопросы 17-30: Да/Нет (1 балл за "Да")
INSERT INTO question_options (question_id, label, points, sort_index)
SELECT q.id,
    'Да',
    1,
    1
FROM questions q
WHERE q.number BETWEEN 17 AND 30
UNION ALL
SELECT q.id,
    'Нет',
    0,
    2
FROM questions q
WHERE q.number BETWEEN 17 AND 30;
-- Вопрос 31: Есть ли у вас отношения?
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 31
        ),
        'Да',
        2,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 31
        ),
        'Не полн',
        1,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 31
        ),
        'Нет',
        0,
        3
    );
-- Вопрос 32: Здоровые ли у вас отношения?
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 32
        ),
        'Да',
        2,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 32
        ),
        'Нет',
        0,
        2
    );
-- Вопросы 33-36: Да/Нет (1 балл за "Да")
INSERT INTO question_options (question_id, label, points, sort_index)
SELECT q.id,
    'Да',
    1,
    1
FROM questions q
WHERE q.number BETWEEN 33 AND 36
UNION ALL
SELECT q.id,
    'Нет',
    0,
    2
FROM questions q
WHERE q.number BETWEEN 33 AND 36;
-- Заполнение вариантов ответов для вопросов категории "Самореализация"
-- Вопросы 37-41: Да/Нет
INSERT INTO question_options (question_id, label, points, sort_index)
SELECT q.id,
    'Да',
    CASE
        WHEN q.number = 41 THEN 2
        ELSE 1
    END,
    1
FROM questions q
WHERE q.number BETWEEN 37 AND 41
UNION ALL
SELECT q.id,
    'Нет',
    0,
    2
FROM questions q
WHERE q.number BETWEEN 37 AND 41;
-- Вопрос 42: Удовлетворены своей работой в бизнесе?
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 42
        ),
        'Да',
        2,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 42
        ),
        'Не полн',
        1,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 42
        ),
        'Нет',
        0,
        3
    );
-- Вопрос 43: Уровень вашего инвестиционного капитала
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 43
        ),
        'До 100 000 руб.',
        0,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 43
        ),
        'От 100 000 до 1 000 000 руб.',
        2,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 43
        ),
        'От 1 000 000 до 3 000 000 руб.',
        4,
        3
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 43
        ),
        'От 3 000 000 до 10 000 000 руб.',
        6,
        4
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 43
        ),
        'От 10 000 000 до 50 000 000 руб.',
        8,
        5
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 43
        ),
        'От 50 000 000 до 100 000 000 руб.',
        10,
        6
    );
-- Вопрос 44: Уровень окружения
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 44
        ),
        'Слабое окружение',
        0,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 44
        ),
        'На вашем уровне',
        5,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 44
        ),
        'Сильное окружение',
        10,
        3
    );
-- Вопрос 45: Уровень активных доходов
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 45
        ),
        'До 10 000 руб./мес.',
        0,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 45
        ),
        'От 10 000 до 50 000 руб./мес.',
        2,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 45
        ),
        'От 50 000 до 100 000 руб./мес.',
        4,
        3
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 45
        ),
        'От 100 000 до 300 000 руб./мес.',
        6,
        4
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 45
        ),
        'От 300 000 до 1 000 000 руб./мес.',
        8,
        5
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 45
        ),
        'От 1 000 000 руб./мес.',
        10,
        6
    );
-- Вопрос 46: Уровень пассивных доходов
INSERT INTO question_options (question_id, label, points, sort_index)
VALUES (
        (
            SELECT id
            FROM questions
            WHERE number = 46
        ),
        'До 10 000 руб./мес.',
        0,
        1
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 46
        ),
        'От 10 000 до 50 000 руб./мес.',
        2,
        2
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 46
        ),
        'От 50 000 до 100 000 руб./мес.',
        4,
        3
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 46
        ),
        'От 100 000 до 300 000 руб./мес.',
        6,
        4
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 46
        ),
        'От 300 000 до 1 000 000 руб./мес.',
        8,
        5
    ),
    (
        (
            SELECT id
            FROM questions
            WHERE number = 46
        ),
        'От 1 000 000 руб./мес.',
        10,
        6
    );
-- Заполнение вариантов ответов для вопросов категории "Свобода"
-- Вопросы 47-51: Да/Нет (2 балла за "Да")
INSERT INTO question_options (question_id, label, points, sort_index)
SELECT q.id,
    'Да',
    2,
    1
FROM questions q
WHERE q.number BETWEEN 47 AND 51
UNION ALL
SELECT q.id,
    'Нет',
    0,
    2
FROM questions q
WHERE q.number BETWEEN 47 AND 51;
-- Проверка корректности данных
SELECT 'Проверка количества вопросов по категориям:' as check_type,
    category,
    COUNT(*) as question_count,
    SUM(max_points) as total_max_points
FROM questions
GROUP BY category
UNION ALL
SELECT 'Общая статистика:' as check_type,
    'ALL' as category,
    COUNT(*) as question_count,
    SUM(max_points) as total_max_points
FROM questions;
-- Проверка вариантов ответов
SELECT 'Проверка вариантов ответов:' as info,
    q.number as question_number,
    q.text as question_text,
    COUNT(qo.id) as options_count
FROM questions q
    LEFT JOIN question_options qo ON q.id = qo.question_id
GROUP BY q.id,
    q.number,
    q.text
ORDER BY q.number;