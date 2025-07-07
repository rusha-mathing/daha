import type {Dispatch, FC, ReactNode, SetStateAction} from "react";

export type Fillable =
    | { kind: "item"; _val: string; _renderer?: FC<ItemRendererProps> }
    | { kind: "array"; _vals: Fillable[]; _renderer?: FC<ArrayRendererProps> }
    | { kind: "object"; _fields: Record<string, Fillable>; _renderer?: FC<ObjectRendererProps> };

export interface ItemRendererProps {
    _val: string;
    setVal: (val: string) => void;
    userData?: unknown;
}

export interface ArrayRendererProps {
    _vals: Fillable[];
    setVals: Dispatch<SetStateAction<Fillable[]>>;
    renderItem: (item: Fillable, index: number) => ReactNode;
    userData?: unknown;
}

export interface ObjectRendererProps {
    _fields: Record<string, Fillable>;
    setFields: (fields: Record<string, Fillable>) => void;
    renderField: (key: string, field: Fillable) => ReactNode;
    userData?: unknown;
}

export type FillableBuilderOptions<T> = {
    itemRenderer?: FC<ItemRendererProps>;
    arrayRenderer?: FC<ArrayRendererProps>;
    objectRenderer?: FC<ObjectRendererProps>;
    userData?: UserDataStringified<T>;
};

export type FillableString = string | [string, FC<ItemRendererProps>];

export type FillableStringified<T> =
    T extends string | number | boolean | null | undefined ? FillableString :
    T extends Array<infer V> ? Array<FillableStringified<V>> :
    T extends object ? { [K in keyof T]: FillableStringified<T[K]> } :
    FillableString;

// New type for userData structure
// Example:
// If T is { name: string, tags: string[], config: { enabled: boolean } }
// Then UserDataStringified<T> is { name?: unknown | undefined, tags?: (unknown | undefined)[], config?: { enabled?: unknown | undefined } }
export type UserDataStringified<T> =
    T extends string | number | boolean | null | undefined ? unknown | undefined:
    T extends Array<infer V> ? Array<UserDataStringified<V>> :
    T extends object ? { [K in keyof T]?: UserDataStringified<T[K]> } :
    unknown | undefined;

export type FillableToValue<T extends Fillable> =
    T extends { kind: "item"; _val: string } ? string :
        T extends { kind: "array"; _vals: infer U } ? U extends Fillable[] ? FillableToValue<U[number]>[] : never :
            T extends {
                    kind: "object";
                    _fields: infer F
                } ? F extends Record<string, Fillable> ? { [K in keyof F & string]: FillableToValue<F[K]> } : never :
                never;