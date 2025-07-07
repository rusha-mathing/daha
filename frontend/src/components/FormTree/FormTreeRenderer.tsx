import {useState, useCallback, useMemo, type FC, useEffect, memo} from "react";
import type {Fillable, ItemRendererProps, ArrayRendererProps, ObjectRendererProps} from "./types";

function isArrayFillable(f: Fillable): f is Extract<Fillable, { kind: 'array' }> {
    return f.kind === 'array';
}

function isObjectFillable(f: Fillable): f is Extract<Fillable, { kind: 'object' }> {
    return f.kind === 'object';
}

function isItemFillable(f: Fillable): f is Extract<Fillable, { kind: 'item' }> {
    return f.kind === 'item';
}

function updateArrayItem(
    arr: Fillable[],
    index: number,
    newItem: Fillable
): Fillable[] {
    const newArr = [...arr];
    newArr[index] = newItem;
    return newArr;
}

function updateObjectField(
    fields: Record<string, Fillable>,
    key: string,
    newField: Fillable
): Record<string, Fillable> {
    return {
        ...fields,
        [key]: newField
    };
}

const FormTreeRendererInner: FC<{
    value: Fillable;
    onChange: (newValue: Fillable) => void;
    userData?: unknown;
}> = ({value, onChange, userData}) => {
    const [localValue, setLocalValue] = useState(value);

    useEffect(() => {
        setLocalValue(value);
    }, [value]);

    const handleChange = useCallback((newVal: Fillable) => {
        setLocalValue(newVal);
        onChange(newVal);
    }, [onChange]);

    // Memoize all possible props/hooks at the top
    const memoVals = useMemo(() => isArrayFillable(localValue) ? localValue._vals : [], [localValue]);
    const memoFields = useMemo(() => isObjectFillable(localValue) ? localValue._fields : {}, [localValue]);
    const memoRenderItem = useCallback(
        (item: Fillable, index: number) => {
            // For arrays, we can pass the userData as is, or index-specific data if needed
            const itemUserData = userData && typeof userData === 'object' && 'items' in userData
                ? (userData as { items: unknown[] }).items?.[index]
                : userData;

            return (
                <FormTreeRenderer
                    key={index}
                    value={item}
                    onChange={newItem => {
                        if (!isArrayFillable(localValue)) return;
                        const updated = {
                            ...localValue,
                            _vals: updateArrayItem(localValue._vals, index, newItem)
                        };
                        handleChange(updated);
                    }}
                    userData={itemUserData}
                />
            );
        },
        [localValue, handleChange, userData]
    );
    const memoSetVals = useCallback(
        (newVals: Fillable[] | ((prev: Fillable[]) => Fillable[])) => {
            if (!isArrayFillable(localValue)) return;
            const nextVals = typeof newVals === "function" ? newVals(localValue._vals) : newVals;
            const updated = {...localValue, _vals: nextVals};
            handleChange(updated);
        },
        [localValue, handleChange]
    );
    const memoRenderField = useCallback(
        (key: string, field: Fillable) => {
            // Get field-specific userData
            const fieldUserData = userData && typeof userData === 'object' && key in userData
                ? (userData as Record<string, unknown>)[key]
                : undefined;

            return (
                <FormTreeRenderer
                    value={field}
                    onChange={newField => {
                        if (!isObjectFillable(localValue)) return;
                        const updated = {
                            ...localValue,
                            _fields: updateObjectField(localValue._fields, key, newField)
                        };
                        handleChange(updated);
                    }}
                    userData={fieldUserData}
                />
            );
        },
        [localValue, handleChange, userData]
    );
    const memoSetFields = useCallback(
        (newFields: Record<string, Fillable>) => {
            if (!isObjectFillable(localValue)) return;
            const updated = {...localValue, _fields: newFields};
            handleChange(updated);
        },
        [localValue, handleChange]
    );

    if (isItemFillable(localValue)) {
        if (!localValue._renderer || typeof localValue._renderer !== 'function') {
            return (
                <input
                    value={localValue._val}
                    onChange={e => {
                        const updated = {...localValue, _val: e.target.value};
                        handleChange(updated);
                    }}
                />
            );
        }
        const Renderer = localValue._renderer as FC<ItemRendererProps>;
        return (
            <Renderer
                _val={localValue._val}
                setVal={newVal => {
                    const updated = {...localValue, _val: newVal};
                    handleChange(updated);
                }}
                userData={userData}
            />
        );
    }
    if (isArrayFillable(localValue)) {
        if (!localValue._renderer || typeof localValue._renderer !== 'function') {
            return (
                <div>
                    {memoVals.map((item, index) => memoRenderItem(item, index))}
                </div>
            );
        }
        const Renderer = localValue._renderer as FC<ArrayRendererProps>;
        return (
            <Renderer
                _vals={memoVals}
                setVals={memoSetVals}
                renderItem={memoRenderItem}
                userData={userData}
            />
        );
    }
    if (isObjectFillable(localValue)) {
        if (!localValue._renderer || typeof localValue._renderer !== 'function') {
            return (
                <div>
                    {Object.entries(memoFields).map(([key, field]) => (
                        <div key={key}>
                            <label>{key}</label>
                            {memoRenderField(key, field)}
                        </div>
                    ))}
                </div>
            );
        }
        const Renderer = localValue._renderer as FC<ObjectRendererProps>;
        return (
            <Renderer
                _fields={memoFields}
                setFields={memoSetFields}
                renderField={memoRenderField}
                userData={userData}
            />
        );
    }
    return null;
};

export const FormTreeRenderer = memo(FormTreeRendererInner);