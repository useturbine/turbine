import { camelCase, isPlainObject, snakeCase } from "lodash";

export const camelizeKeys = <
  T extends Record<string, unknown> | Record<string, unknown>[]
>(
  obj: T
): T => {
  if (Array.isArray(obj)) {
    return <T>obj.map((v) => camelizeKeys(v));
  } else if (isPlainObject(obj)) {
    return <T>Object.keys(obj).reduce(
      (result, key) => ({
        ...result,
        [camelCase(key)]: camelizeKeys(<T>obj[key]),
      }),
      {}
    );
  }
  return obj;
};

export const snakeifyKeys = <
  T extends Record<string, unknown> | Record<string, unknown>[]
>(
  obj: T
): T => {
  if (Array.isArray(obj)) {
    return <T>obj.map((v) => snakeifyKeys(v));
  } else if (isPlainObject(obj)) {
    return <T>Object.keys(obj).reduce(
      (result, key) => ({
        ...result,
        [snakeCase(key)]: snakeifyKeys(<T>obj[key]),
      }),
      {}
    );
  }
  return obj;
};
