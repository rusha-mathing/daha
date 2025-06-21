import type {Difficulty, Resource, Subject} from "./types.ts";

export function getDifficulties(): Array<Difficulty> {
    return [
        {
            "type": "beginner",
            "label": "начальный",
            "icon": `<path d="M5 13.18v4L12 21l7-3.82v-4L12 17zM12 3 1 9l11 6 9-4.91V17h2V9z"></path>`,
            "color": "#4caf50",
        },
        {
            "type": "intermediate",
            "label": "средний",
            "icon": `<path d="m16 6 2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"></path>`,
            "color": "#ff9800",
        },
        {
            "type": "advanced",
            "label": "продвинутый",
            "icon": `<path d="M13 8.57c-.79 0-1.43.64-1.43 1.43s.64 1.43 1.43 1.43 1.43-.64 1.43-1.43-.64-1.43-1.43-1.43"></path><path d="M13 3C9.25 3 6.2 5.94 6.02 9.64L4.1 12.2c-.25.33-.01.8.4.8H6v3c0 1.1.9 2 2 2h1v3h7v-4.68c2.36-1.12 4-3.53 4-6.32 0-3.87-3.13-7-7-7m3 7c0 .13-.01.26-.02.39l.83.66c.08.06.1.16.05.25l-.8 1.39c-.05.09-.16.12-.24.09l-.99-.4c-.21.16-.43.29-.67.39L14 13.83c-.01.1-.1.17-.2.17h-1.6c-.1 0-.18-.07-.2-.17l-.15-1.06c-.25-.1-.47-.23-.68-.39l-.99.4c-.09.03-.2 0-.25-.09l-.8-1.39c-.05-.08-.03-.19.05-.25l.84-.66c-.01-.13-.02-.26-.02-.39s.02-.27.04-.39l-.85-.66c-.08-.06-.1-.16-.05-.26l.8-1.38c.05-.09.15-.12.24-.09l1 .4c.2-.15.43-.29.67-.39L12 6.17c.02-.1.1-.17.2-.17h1.6c.1 0 .18.07.2.17l.15 1.06c.24.1.46.23.67.39l1-.4c.09-.03.2 0 .24.09l.8 1.38c.05.09.03.2-.05.26l-.85.66c.03.12.04.25.04.39"></path>`,
            "color": "#f44336",
        },
    ];
}

function setupGetDifficulty(): (type: string) => Difficulty | undefined {
    const map: Map<string, Difficulty> = new Map();
    const difficulties: Array<Difficulty> = getDifficulties();
    for (const difficulty of difficulties) {
        map.set(difficulty.type, difficulty);
    }
    return ((type: string): Difficulty | undefined => {
        return map.get(type);
    })
}

export const getDifficulty: (type: string) => Difficulty | undefined = setupGetDifficulty();

export function getSubjects(): Array<Subject> {
    return [
        {
            "type": "ai",
            "label": "Искусственный интеллект",
            "icon": `<path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3M7.5 11.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5S9.83 13 9 13s-1.5-.67-1.5-1.5M16 17H8v-2h8zm-1-4c-.83 0-1.5-.67-1.5-1.5S14.17 10 15 10s1.5.67 1.5 1.5S15.83 13 15 13"></path>`,
            "color": "#3f51b5",
            "additionalDescription": [
                'Слушатели осваивают практические навыки построения нейронных сетей и работы с большими данными.',
                'Курс включает работу с реальными проектами и актуальными инструментами искусственного интеллекта.'
            ],
        },
        {
            "type": "robotics",
            "label": "Робототехника",
            "icon": `<path d="m19.93 8.21-3.6 1.68L14 7.7V6.3l2.33-2.19 3.6 1.68c.38.18.82.01 1-.36.18-.38.01-.82-.36-1L16.65 2.6c-.38-.18-.83-.1-1.13.2l-1.74 1.6c-.18-.24-.46-.4-.78-.4-.55 0-1 .45-1 1v1H8.82C8.34 4.65 6.98 3.73 5.4 4.07c-1.16.25-2.15 1.25-2.36 2.43-.22 1.32.46 2.47 1.48 3.08L7.08 18H4v3h13v-3h-3.62L8.41 8.77c.17-.24.31-.49.41-.77H12v1c0 .55.45 1 1 1 .32 0 .6-.16.78-.4l1.74 1.6c.3.3.75.38 1.13.2l3.92-1.83c.38-.18.54-.62.36-1-.18-.37-.62-.54-1-.36M6 8c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1"></path>`,
            "color": "#9c27b0",
            "additionalDescription": [
                'Слушатели осваивают практические навыки построения нейронных сетей и работы с большими данными.',
                'Курс включает работу с реальными проектами и актуальными инструментами искусственного интеллекта.'
            ],
        },
        {
            "type": "programming",
            "label": "Программирование",
            "icon": `<path d="M9.4 16.6 4.8 12l4.6-4.6L8 6l-6 6 6 6zm5.2 0 4.6-4.6-4.6-4.6L16 6l6 6-6 6z"></path>`,
            "color": "#00bfa5",
            "additionalDescription": [
                'Обучение строится на решении практических задач с постепенным повышением сложности.',
                'Участники научатся писать оптимальный и читаемый код, работая над реальными проектами.'
            ],
        },
        {
            "type": "cybersecurity",
            "label": "Информационная безопасность",
            "icon": `<path d="M12 1 3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11z"></path>`,
            "color": "#f44336",
            "additionalDescription": [
                'Изучаются методы защиты информации и противодействия современным киберугрозам.',
                'Курс дает практические навыки обнаружения уязвимостей и построения защищенных систем.'
            ],
        },
        {
            "type": "entrepreneurship",
            "label": "Предпринимательство",
            "icon": `<path d="M12 7V3H2v18h20V7zM6 19H4v-2h2zm0-4H4v-2h2zm0-4H4V9h2zm0-4H4V5h2zm4 12H8v-2h2zm0-4H8v-2h2zm0-4H8V9h2zm0-4H8V5h2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8zm-2-8h-2v2h2zm0 4h-2v2h2z"></path>`,
            "color": "#ff9800",
            "additionalDescription": [
                'Слушатели разработают собственный бизнес-план и изучат стратегии привлечения инвестиций.',
                'В программу включены мастер-классы от успешных предпринимателей и венчурных инвесторов.'
            ],
        },
        {
            "type": "financial_literacy",
            "label": "Финансовая грамотность",
            "icon": `<path d="M4 10h3v7H4zm6.5 0h3v7h-3zM2 19h20v3H2zm15-9h3v7h-3zm-5-9L2 6v2h20V6z"></path>`,
            "color": "#2196f3",
            "additionalDescription": [
                'Участники научатся эффективно управлять личными финансами и создавать пассивный доход.',
                'Курс включает разбор реальных инвестиционных стратегий и финансовых инструментов.'
            ],
        },
        {
            "type": "science",
            "label": "Наука",
            "icon": `<path d="M19.8 18.4 14 10.67V6.5l1.35-1.69c.26-.33.03-.81-.39-.81H9.04c-.42 0-.65.48-.39.81L10 6.5v4.17L4.2 18.4c-.49.66-.02 1.6.8 1.6h14c.82 0 1.29-.94.8-1.6"></path>`,
            "color": "#4caf50",
            "additionalDescription": [
                'Программа сочетает теоретическую подготовку с практическими экспериментами и исследованиями.',
                'Участники работают с современным научным оборудованием под руководством ученых-практиков.'
            ],
        },
    ];
}


function setupGetSubject(): (type: string) => Subject | undefined {
    const map: Map<string, Subject> = new Map();
    const subjects: Array<Subject> = getSubjects();
    for (const difficulty of subjects) {
        map.set(difficulty.type, difficulty);
    }
    return ((type: string): Subject | undefined => {
        return map.get(type);
    })
}

export const getSubject: (type: string) => Subject | undefined = setupGetSubject();


export function getGrades(): Array<string> {
    return ["7", "8", "9", "10", "11"];
}


export const resources: Resource[] = [{
    id: '1',
    title: 'Основы машинного обучения и нейронных сетей',
    description: 'Ведут специалисты из Яндекса с реальными кейсами из индустрии.',
    subjectTypes: ["ai"],
    grades: ["10", "11"],
    startDate: '2025-09-15',
    endDate: '2026-01-20',
    url: 'https://practicum.yandex.ru/',
    imageUrl: 'https://placehold.co/100x100?text=AI',
    organizer: 'Яндекс',
    difficultyLevel: 'intermediate',
}, {
    id: '2',
    title: 'Python для искусственного интеллекта',
    description: 'Поможет подготовиться к участию в олимпиадах по программированию.',
    subjectTypes: ["ai", "programming"],
    grades: ["9", "10", "11"],
    startDate: '2025-10-01',
    endDate: '2026-02-28',
    url: 'https://stepik.org/',
    imageUrl: 'https://placehold.co/100x100?text=Python+AI',
    organizer: 'Сириус',
    difficultyLevel: 'beginner',
}, {
    id: '3',
    title: 'Робототехника для начинающих',
    description: 'Включает практические занятия со сборкой реальных роботов.',
    subjectTypes: ["robotics"],
    grades: ["7", "8", "9"],
    startDate: '2025-09-01',
    endDate: '2025-12-20',
    url: 'https://robbo.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Robotics',
    organizer: 'Иннополис',
    difficultyLevel: 'beginner',
}, {
    id: '4',
    title: 'Программирование микроконтроллеров Arduino',
    description: 'После курса сможешь создавать собственные устройства умного дома.',
    subjectTypes: ["robotics", "programming"],
    grades: ["8", "9", "10"],
    startDate: '2025-10-05',
    endDate: '2026-02-10',
    url: 'https://amperka.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Arduino',
    organizer: 'Сколтех',
    difficultyLevel: 'beginner',
}, {
    id: '5',
    title: 'Разработка игр на Unity',
    description: 'Возможность добавить проекты в портфолио для будущих работодателей.',
    subjectTypes: ["programming"],
    grades: ["8", "9", "10", "11"],
    startDate: '2025-09-15',
    endDate: '2026-01-30',
    url: 'https://unity.com/learn',
    imageUrl: 'https://placehold.co/100x100?text=Unity',
    organizer: 'VK',
    difficultyLevel: 'intermediate',
}, {
    id: '6',
    title: 'Основы кибербезопасности',
    description: 'Преподают действующие эксперты по информационной безопасности.',
    subjectTypes: ["cybersecurity"],
    grades: ["9", "10", "11"],
    startDate: '2025-09-10',
    endDate: '2025-12-15',
    url: 'https://securitytrainings.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Security',
    organizer: 'СберКибер',
    difficultyLevel: 'beginner',
}, {
    id: '7',
    title: 'Этичный хакинг и тестирование на проникновение',
    description: 'Помогает развить аналитическое мышление и внимание к деталям.',
    subjectTypes: ["cybersecurity", "programming"],
    grades: ["10", "11"],
    startDate: '2025-10-20',
    endDate: '2026-02-15',
    url: 'https://skillbox.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Hacking',
    organizer: 'Лаборатория Касперского',
    difficultyLevel: 'advanced',
}, {
    id: '8',
    title: 'Предпринимательство для школьников',
    description: 'Возможность запустить свой первый бизнес-проект под наставничеством.',
    subjectTypes: ["entrepreneurship"],
    grades: ["8", "9", "10", "11"],
    startDate: '2025-09-05',
    endDate: '2025-12-10',
    url: 'https://business-youth.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Business',
    organizer: 'Высшая школа экономики',
    difficultyLevel: 'beginner',
}, {
    id: '9',
    title: 'От идеи до стартапа',
    description: 'Шанс получить финансирование от инвесторов для лучших проектов.',
    subjectTypes: ["entrepreneurship"],
    grades: ["9", "10", "11"],
    startDate: '2025-10-10',
    endDate: '2026-03-20',
    url: 'https://practicumglobal.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Startup',
    organizer: 'Сколково',
    difficultyLevel: 'intermediate',
}, {
    id: '10',
    title: 'Личные финансы для подростков',
    description: 'Научит грамотно управлять своим бюджетом и планировать накопления.',
    subjectTypes: ["financial_literacy"],
    grades: ["7", "8", "9", "10", "11"],
    startDate: '2025-09-15',
    endDate: '2025-11-30',
    url: 'https://fincult.info/',
    imageUrl: 'https://placehold.co/100x100?text=Finance',
    organizer: 'Центральный банк РФ',
    difficultyLevel: 'beginner',
}, {
    id: '11',
    title: 'Инвестирование для начинающих',
    description: 'Практические навыки работы с биржевыми инструментами на учебном счете.',
    subjectTypes: ["financial_literacy"],
    grades: ["10", "11"],
    startDate: '2025-10-05',
    endDate: '2026-01-25',
    url: 'https://www.tinkoff.ru/invest/education/',
    imageUrl: 'https://placehold.co/100x100?text=Invest',
    organizer: 'Тинькофф',
    difficultyLevel: 'intermediate',
}, {
    id: '12',
    title: 'Современная физика для школьников',
    description: 'Поможет подготовиться к олимпиадам и поступлению в технические вузы.',
    subjectTypes: ["science"],
    grades: ["9", "10", "11"],
    startDate: '2025-09-01',
    endDate: '2026-04-30',
    url: 'https://mipt.ru/online-courses/',
    imageUrl: 'https://placehold.co/100x100?text=Physics',
    organizer: 'МФТИ',
    difficultyLevel: 'advanced',
}, {
    id: '13',
    title: 'Экспериментальная химия',
    description: 'Доступ к лабораториям с современным оборудованием.',
    subjectTypes: ["science"],
    grades: ["8", "9", "10", "11"],
    startDate: '2025-09-20',
    endDate: '2026-03-15',
    url: 'https://chemgood.ru/courses/',
    imageUrl: 'https://placehold.co/100x100?text=Chemistry',
    organizer: 'МГУ им. Ломоносова',
    difficultyLevel: 'intermediate',
}, {
    id: '14',
    title: 'Биология будущего',
    description: 'Включает экскурсии в исследовательские центры и работу с учеными.',
    subjectTypes: ["science"],
    grades: ["9", "10", "11"],
    startDate: '2025-10-01',
    endDate: '2026-02-28',
    url: 'https://biomolecula.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Biology',
    organizer: 'Летово',
    difficultyLevel: 'intermediate',
}, {
    id: '15',
    title: 'Астрономия и космические технологии',
    description: 'Возможность наблюдать за небесными телами через профессиональные телескопы.',
    subjectTypes: ["science"],
    grades: ["7", "8", "9", "10", "11"],
    startDate: '2025-09-10',
    endDate: '2026-04-10',
    url: 'https://www.planetarium-moscow.ru/about/about/',
    imageUrl: 'https://placehold.co/100x100?text=Astronomy',
    organizer: 'Сириус',
    difficultyLevel: 'beginner',
}, {
    id: '16',
    title: 'Веб-разработка для начинающих',
    description: 'Сертификат признается IT-компаниями при приеме на стажировку.',
    subjectTypes: ["programming"],
    grades: ["8", "9", "10", "11"],
    startDate: '2025-09-05',
    endDate: '2025-12-20',
    url: 'https://htmlacademy.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Web',
    organizer: 'Яндекс',
    difficultyLevel: 'beginner',
}, {
    id: '17',
    title: 'Криптография и защита данных',
    description: 'Разработан совместно с лабораторией Касперского.',
    subjectTypes: ["cybersecurity", "programming"],
    grades: ["10", "11"],
    startDate: '2025-10-15',
    endDate: '2026-02-10',
    url: 'https://academy.kaspersky.ru/',
    imageUrl: 'https://placehold.co/100x100?text=Crypto',
    organizer: 'Высшая школа экономики',
    difficultyLevel: 'advanced',
}, {
    id: '18',
    title: 'Компьютерное зрение и распознавание образов',
    description: 'Занятия проходят на оборудовании, используемом в реальных проектах.',
    subjectTypes: ["ai", "programming"],
    grades: ["10", "11"],
    startDate: '2025-09-20',
    endDate: '2026-01-30',
    url: 'https://neural-university.ru/',
    imageUrl: 'https://placehold.co/100x100?text=ComputerVision',
    organizer: 'Сбер',
    difficultyLevel: 'advanced',
},];