import type {Subject} from "../../types/filters/subject.ts";

export const formatDate = (dateString: string) => {
    if (!dateString.length) return "";
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return "";
    const day = date.getDate();
    const year = date.getFullYear();

    const monthsGenitive = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ];

    const month = monthsGenitive[date.getMonth()];
    return `${day} ${month} ${year}`;
};

export const getEnhancedDescription = (
    primarySubject?: Subject,
    description?: string,
) => {
    if (description?.length && description.length> 150) return description;

    let formattedDescription = description;

    if (formattedDescription &&
        !formattedDescription.endsWith('.') &&
        !formattedDescription.endsWith('!') &&
        !formattedDescription.endsWith('?')) {
        formattedDescription += '.';
    }
    const additions = primarySubject?.additional_description;
    if (additions && additions.length) {
        return `${formattedDescription} ${additions.join(' ')}`;
    }

    // if (!formattedDescription || !formattedDescription.length) return ''
    return `${formattedDescription} Программа разработана ведущими специалистами с учетом современных требований отрасли. Участники получат актуальные знания и ценные практические навыки.`;
};

export const capitalize = (text: string) => {
    return text.charAt(0).toUpperCase() + text.slice(1);
}