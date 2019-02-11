/**
 * Defines the global Typescript condition interfaces for the React front-end
 */

import { Indicator } from "./indicators";

export enum Comparator {
    GT = ">",
    EQ = "=",
    LT = "<"
}

export enum ConditionType {
    BUY,
    SELL
}

export interface Condition {
    leftSide?: Indicator,
    comparator: Comparator,
    rightSide?: Indicator
}

export type BacktestPayload = {coinPair: string,
                               timeUnit: string,
                               capital: number,
                               stopLoss: number,
                               startTime: number,
                               buyStrategy: object,
                               sellStrategy: object,
                               indicators: string[]}

export type BacktestData = {time: number, close: number, buy?: number, sell?: number, indicators?: object[]}