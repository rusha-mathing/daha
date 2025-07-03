import type {FC} from 'react';
import {SvgIcon, type SvgIconProps} from '@mui/material';
import DOMPurify from 'dompurify';

interface DynamicSvgProps extends SvgIconProps {
    fontSize?: "small" | "inherit" | "large" | "medium";
    svg: string;
    viewBox?: string;
}

const DynamicSvg: FC<DynamicSvgProps> = ({fontSize, svg, viewBox = '0 0 24 24', ...svgIconProps}) => {
    const sanitizedSvg = DOMPurify.sanitize(svg, {
        USE_PROFILES: {svg: true},
        ALLOWED_TAGS: ['path', 'circle', 'rect', 'g', 'line', 'polyline', 'polygon'],
        ALLOWED_ATTR: ['d', 'fill', 'stroke', 'stroke-width', 'cx', 'cy', 'r', 'x', 'y', 'width', 'height'],
    });

    return (
        <SvgIcon fontSize={fontSize} viewBox={viewBox} {...svgIconProps}>
            <g dangerouslySetInnerHTML={{__html: sanitizedSvg}}/>
        </SvgIcon>
    );
};

export default DynamicSvg;