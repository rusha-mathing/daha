import {useMemo, useState, type FC, useCallback, useRef} from "react";
import type {
    Fillable,
    FillableBuilderOptions,
    FillableStringified,
    FillableToValue,
    UserDataStringified
} from "./types";

function isFillable(val: unknown): val is Fillable {
    return typeof val === "object" && val !== null && "kind" in val;
}

export function makeFillable<T>(
    value: T,
    options: FillableBuilderOptions<T> = {}
): Fillable {
    if (Array.isArray(value) && value.length === 2 && typeof value[1] === "function") {
        const [val, renderer] = value as [unknown, FC<unknown>];
        if (Array.isArray(val)) {
            return {
                kind: "array",
                _vals: val.map((v) => makeFillable(v, options)),
                _renderer: renderer,
            };
        } else if (typeof val === "object" && val !== null) {
            const fields: Record<string, Fillable> = {};
            for (const key of Object.keys(val)) {
                fields[key] = makeFillable((val as Record<string, unknown>)[key], options);
            }
            return {
                kind: "object",
                _fields: fields,
                _renderer: renderer,
            };
        } else {
            return {
                kind: "item",
                _val: String(val),
                _renderer: renderer,
            };
        }
    }
    if (Array.isArray(value)) {
        return {
            kind: "array",
            _vals: value.map((v) => makeFillable(v, options)),
            ...(options.arrayRenderer ? {_renderer: options.arrayRenderer} : {}),
        };
    } else if (typeof value === "object" && value !== null) {
        // If already a Fillable, return as is
        if (isFillable(value)) return value;
        const fields: Record<string, Fillable> = {};
        for (const key of Object.keys(value)) {
            fields[key] = makeFillable((value as Record<string, unknown>)[key], options);
        }
        return {
            kind: "object",
            _fields: fields,
            ...(options.objectRenderer ? {_renderer: options.objectRenderer} : {}),
        };
    } else {
        return {
            kind: "item",
            _val: String(value),
            ...(options.itemRenderer ? {_renderer: options.itemRenderer} : {}),
        };
    }
}

export function extractValueFromFillable<T extends Fillable>(fillable: T): FillableToValue<T> {
    switch (fillable.kind) {
        case "item":
            return fillable._val as FillableToValue<T>;
        case "array":
            return fillable._vals.map(extractValueFromFillable) as FillableToValue<T>;
        case "object": {
            const result = {} as { [K in keyof typeof fillable._fields & string]: unknown };
            for (const key of Object.keys(fillable._fields)) {
                result[key as keyof typeof fillable._fields & string] = extractValueFromFillable(fillable._fields[key]);
            }
            return result as FillableToValue<T>;
        }
        default:
            throw new Error('Unknown fillable kind');
    }
}

export function useFormTree<T, S = FillableStringified<T>, R = T, U = UserDataStringified<T>>(
    initialValue: S,
    options: FillableBuilderOptions<S> & { userData?: U } = {},
    castFunction?: (value: S) => R
) {
    // Store initial and options in refs to ensure reset always uses the originals
    const initialRef = useRef(initialValue);
    const optionsRef = useRef(options);

    const [fillable, setFillable] = useState<Fillable>(() => makeFillable(initialValue, options));
    const value = useMemo(() => {
        const extractedValue = extractValueFromFillable(fillable) as S;
        return castFunction ? castFunction(extractedValue) as R : (extractedValue as S);
    }, [fillable, castFunction]);

    // Add a reset function
    const reset = useCallback(() => {
        setFillable(makeFillable(initialRef.current, optionsRef.current));
    }, []);

    return {fillable, setFillable, reset, value};
}