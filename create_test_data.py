from datetime import date

from sqlalchemy.orm import Session

from app.models import (
    create_db_and_models,
    engine,
    Subject,
    Difficulty,
    Grade,
    Course,
    CourseSubjectLink,
    CourseGradeLink,
    Organization,
)


def main():
    create_db_and_models()
    with Session(engine) as session:
        # defining subjects
        subject_1 = Subject(
            type='test1',
            label='Тестовое направление 1',
            icon="""<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 512 512" xml:space="preserve">
<polygon style="fill:#E09B2D;" points="356.648,9.866 432.636,85.867 356.648,85.867 "/>
<g>
	<rect x="127.073" y="111.93" style="fill:#F95428;" width="56.57" height="50.084"/>
	<rect x="127.073" y="203.548" style="fill:#F95428;" width="56.57" height="50.084"/>
</g>
<path style="fill:#F7B239;" d="M432.636,85.867v416.265H79.361V9.866h277.286v76.001H432.636z M183.648,436.879v-50.084h-56.57
	v50.084H183.648z M183.648,345.261v-50.084h-56.57v50.084H183.648z M183.648,253.631v-50.084h-56.57v50.084H183.648z
	 M183.648,162.013v-50.084h-56.57v50.084H183.648z"/>
<g>
	<rect x="127.073" y="386.796" style="fill:#F95428;" width="56.57" height="50.084"/>
	<rect x="127.073" y="295.178" style="fill:#F95428;" width="56.57" height="50.084"/>
</g>
<g>
	<path style="fill:#FFFFFF;" d="M400.72,475.399c-5.45,0-9.867-4.418-9.867-9.867v-313.11c0-5.449,4.416-9.867,9.867-9.867
		c5.451,0,9.867,4.418,9.867,9.867v313.11C410.587,470.981,406.169,475.399,400.72,475.399z"/>
	<circle style="fill:#FFFFFF;" cx="400.715" cy="119.534" r="9.867"/>
</g>
<g>
	<path style="fill:#333333;" d="M439.615,78.892L363.627,2.89c-1.85-1.85-4.36-2.89-6.978-2.89H79.363
		c-5.45,0-9.867,4.418-9.867,9.867v492.266c0,5.449,4.416,9.867,9.867,9.867h353.275c5.45,0,9.867-4.418,9.867-9.867V85.868
		C442.504,83.252,441.465,80.743,439.615,78.892z M366.516,33.691l42.304,42.311h-42.304V33.691z M89.23,492.266V19.734h257.554
		v66.135c0,5.449,4.416,9.867,9.867,9.867h66.121v396.531H89.23z"/>
	<path style="fill:#333333;" d="M183.645,102.063h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867V111.93C193.512,106.481,189.095,102.063,183.645,102.063z M173.778,152.145h-36.836v-30.348
		h36.836V152.145z"/>
	<path style="fill:#333333;" d="M352.557,125.357H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,125.357,352.557,125.357z"/>
	<path style="fill:#333333;" d="M183.645,193.686h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867v-50.082C193.512,198.104,189.095,193.686,183.645,193.686z M173.778,243.768h-36.836V213.42
		h36.836V243.768z"/>
	<path style="fill:#333333;" d="M352.557,216.98H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,216.98,352.557,216.98z"/>
	<path style="fill:#333333;" d="M183.645,285.309h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867v-50.082C193.512,289.726,189.095,285.309,183.645,285.309z M173.778,335.39h-36.836v-30.348
		h36.836V335.39z"/>
	<path style="fill:#333333;" d="M352.557,308.602H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,308.602,352.557,308.602z"/>
	<path style="fill:#333333;" d="M183.645,376.931h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867v-50.082C193.512,381.349,189.095,376.931,183.645,376.931z M173.778,427.013h-36.836
		v-30.348h36.836V427.013z"/>
	<path style="fill:#333333;" d="M352.557,400.225H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,400.225,352.557,400.225z"/>
</g>
</svg>""",
            color='#ff0000',
            additional_description=[
                'Описание 1',
                'Описание 2',
            ],
        )

        subject_2 = Subject(
            type='test2',
            label='Тестовое направление 2',
            icon="""<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 512 512" xml:space="preserve">
<polygon style="fill:#E09B2D;" points="356.648,9.866 432.636,85.867 356.648,85.867 "/>
<g>
	<rect x="127.073" y="111.93" style="fill:#F95428;" width="56.57" height="50.084"/>
	<rect x="127.073" y="203.548" style="fill:#F95428;" width="56.57" height="50.084"/>
</g>
<path style="fill:#F7B239;" d="M432.636,85.867v416.265H79.361V9.866h277.286v76.001H432.636z M183.648,436.879v-50.084h-56.57
	v50.084H183.648z M183.648,345.261v-50.084h-56.57v50.084H183.648z M183.648,253.631v-50.084h-56.57v50.084H183.648z
	 M183.648,162.013v-50.084h-56.57v50.084H183.648z"/>
<g>
	<rect x="127.073" y="386.796" style="fill:#F95428;" width="56.57" height="50.084"/>
	<rect x="127.073" y="295.178" style="fill:#F95428;" width="56.57" height="50.084"/>
</g>
<g>
	<path style="fill:#FFFFFF;" d="M400.72,475.399c-5.45,0-9.867-4.418-9.867-9.867v-313.11c0-5.449,4.416-9.867,9.867-9.867
		c5.451,0,9.867,4.418,9.867,9.867v313.11C410.587,470.981,406.169,475.399,400.72,475.399z"/>
	<circle style="fill:#FFFFFF;" cx="400.715" cy="119.534" r="9.867"/>
</g>
<g>
	<path style="fill:#333333;" d="M439.615,78.892L363.627,2.89c-1.85-1.85-4.36-2.89-6.978-2.89H79.363
		c-5.45,0-9.867,4.418-9.867,9.867v492.266c0,5.449,4.416,9.867,9.867,9.867h353.275c5.45,0,9.867-4.418,9.867-9.867V85.868
		C442.504,83.252,441.465,80.743,439.615,78.892z M366.516,33.691l42.304,42.311h-42.304V33.691z M89.23,492.266V19.734h257.554
		v66.135c0,5.449,4.416,9.867,9.867,9.867h66.121v396.531H89.23z"/>
	<path style="fill:#333333;" d="M183.645,102.063h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867V111.93C193.512,106.481,189.095,102.063,183.645,102.063z M173.778,152.145h-36.836v-30.348
		h36.836V152.145z"/>
	<path style="fill:#333333;" d="M352.557,125.357H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,125.357,352.557,125.357z"/>
	<path style="fill:#333333;" d="M183.645,193.686h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867v-50.082C193.512,198.104,189.095,193.686,183.645,193.686z M173.778,243.768h-36.836V213.42
		h36.836V243.768z"/>
	<path style="fill:#333333;" d="M352.557,216.98H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,216.98,352.557,216.98z"/>
	<path style="fill:#333333;" d="M183.645,285.309h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867v-50.082C193.512,289.726,189.095,285.309,183.645,285.309z M173.778,335.39h-36.836v-30.348
		h36.836V335.39z"/>
	<path style="fill:#333333;" d="M352.557,308.602H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,308.602,352.557,308.602z"/>
	<path style="fill:#333333;" d="M183.645,376.931h-56.57c-5.45,0-9.867,4.418-9.867,9.867v50.082c0,5.449,4.416,9.867,9.867,9.867
		h56.57c5.45,0,9.867-4.418,9.867-9.867v-50.082C193.512,381.349,189.095,376.931,183.645,376.931z M173.778,427.013h-36.836
		v-30.348h36.836V427.013z"/>
	<path style="fill:#333333;" d="M352.557,400.225H232.321c-5.45,0-9.867,4.418-9.867,9.867s4.416,9.867,9.867,9.867h120.237
		c5.45,0,9.867-4.418,9.867-9.867S358.008,400.225,352.557,400.225z"/>
</g>
</svg>""",
            color='#00ff00',
            additional_description=[
                'Описание 1',
                'Описание 2',
            ],
        )
        session.add_all([subject_1, subject_2])
        session.commit()  # .id

        # defining difficulties
        difficulty_beginner = Difficulty(
            type='beginner',
            label='начальный',
            icon='<path d="M5 13.18v4L12 21l7-3.82v-4L12 17zM12 3 1 9l11 6 9-4.91V17h2V9z"></path>',
            color='#4caf50',
        )
        difficulty_intermediate = Difficulty(
            type='intermediate',
            label='средний',
            icon='<path d="m16 6 2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"></path>',
            color='#ff9800',
        )
        session.add_all([difficulty_beginner, difficulty_intermediate])
        session.commit()  # .id

        # defining grades
        grade_8 = Grade(grade=8)
        grade_9 = Grade(grade=9)
        grade_10 = Grade(grade=10)
        grade_11 = Grade(grade=11)
        session.add_all(
            [
                grade_8,
                grade_9,
                grade_10,
                grade_11,
            ]
        )
        session.commit()  # .id

        # define organizations
        def define_organization(name):
            org = Organization(name=name)
            session.add(org)
            session.commit()  # .id
            return org

        org_yandex = define_organization('Яндекс')
        org_sirius = define_organization('Сириус')
        org_inno = define_organization('Иннополис')
        org_skoltex = define_organization('Сколтех')
        org_vk = define_organization('VK')
        org_sbercyber = define_organization('СберКибер')
        org_kaspersky = define_organization('Лаборатория Касперского')
        org_cse = define_organization('Высшая школа экономики')
        org_skolkovo = define_organization('Сколково')
        org_cbrf = define_organization('Центральный банк РФ')
        org_tinkoff = define_organization('Тинькофф')
        org_mfti = define_organization('МФТИ')
        org_msu = define_organization('МГУ им. Ломоносова')
        org_letovo = define_organization('Летово')
        org_sber = define_organization('Сбер')
        org_test = define_organization('Тест')

        # defining courses based on what was defined earlier
        def define_course(
            title,
            description,
            subjects,
            grades,
            start_date,
            end_date,
            url,
            image_url,
            organization,
            difficulty,
        ):
            course = Course(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                url=url,
                image_url=image_url,
                organization_id=organization.id,
                difficulty_id=difficulty.id,
                subject_ids=[i.id for i in subjects],
                grade_ids=[i.id for i in grades],
            )
            session.add(course)
            session.commit()  # .id

            for subject in subjects:
                session.add(CourseSubjectLink(course_id=course.id, subject_id=subject.id))
            for grade in grades:
                session.add(CourseGradeLink(course_id=course.id, grade_id=grade.id))
            session.commit()
            return course

        define_course(
            title='Основы машинного обучения и нейронных сетей',
            description='Ведут специалисты из Яндекса с реальными кейсами из индустрии.',
            subjects=[subject_1],
            grades=[grade_10, grade_11],
            start_date=date(2025, 9, 15),
            end_date=date(2026, 1, 20),
            url='https://practicum.yandex.ru/',
            image_url='https://placehold.co/100x100?text=AI',
            organization=org_yandex,
            difficulty=difficulty_intermediate,
        )
        define_course(
            title='Python для искусственного интеллекта',
            description='Поможет подготовиться к участию в олимпиадах по программированию.',
            subjects=[subject_2, subject_1],
            grades=[grade_9, grade_10, grade_11],
            start_date=date(2025, 10, 1),
            end_date=date(2026, 2, 28),
            url='https://stepik.org/',
            image_url='https://placehold.co/100x100?text=Python+AI',
            organization=org_test,
            difficulty=difficulty_beginner,
        )


if __name__ == '__main__':
    main()
