/**
 * Defines the global Typescript indicator interfaces for the React front-end
 */

export interface Indicator {
    // The first data point is the x-axis, then remaining are y-axis
    dataPoints: [number, ...number[]][],
    jsonRepr: () => string
}

/**
 * Defines a class for the current price indicator
 */
class CurrentPrice implements Indicator {

    public dataPoints: [number, number][];

    constructor(data?: [number, number][]) {
        this.dataPoints = data ? data : [];
    }

    /**
     * Return the serialized representation of this indicator
     */
    jsonRepr() {
        return "currentprice";
    }

    toString() {
        return "Current Price";
    }
}

/**
 * Defines a class for the simple moving average indicator
 * TODO(jbartola): Add support for exponential moving average
 */
class MovingAverage implements Indicator {

    readonly period: number;
    public dataPoints: [number, number][];


    constructor(period: number, data?: [number, number][]) {
        this.period = period;
        this.dataPoints = data ? data : [];
    }

    /**
     * Return the serialized representation of this indicator
     */
    jsonRepr() {
        return `sma-${this.period}`;
    }

    toString() {
        return `Moving Average (${this.period} Period)`;
    }
}

/**
 * Defines a class for the Bollinger Band indicator
 */
class Bollinger implements Indicator {

    readonly period: number;
    readonly stdDev: number;
    public dataPoints: [number, number, number, number][];


    constructor(period: number, stdDev: number, data?: [number, number, number, number][]) {
        this.period = period;
        this.stdDev = stdDev;
        this.dataPoints = data ? data : [];
    }

    /**
     * Return the serialized representation of this indicator
     */
    jsonRepr() {
        return `bollinger-${this.period}-${this.stdDev}`;
    }

    toString() {
        return `Bollinger Bands (${this.period} Period)`;
    }
}

/**
 * Defines a class for the RSI indicator
 */
class RSI implements Indicator {

    readonly period: number;
    public dataPoints: [number, number][];


    constructor(period: number, data?: [number, number][]) {
        this.period = period;
        this.dataPoints = data ? data : [];
    }

    /**
     * Return the serialized representation of this indicator
     */
    jsonRepr() {
        return `rsi-${this.period}`;
    }

    toString() {
        return `RSI (${this.period} Period)`;
    }
}

/** Defines the default indicators that will be loaded on startup of the application **/
export const DEFAULT_INDICATORS = [new CurrentPrice(),
                                   new MovingAverage(9),
                                   new MovingAverage(15),
                                   new Bollinger(20, 2),
                                   new RSI(14)];

// Maps indicator JSON representations to their class instances
export const INDICATOR_MAP = new Map<string, Indicator>([
...DEFAULT_INDICATORS.map(i => [i.jsonRepr(), i as Indicator]) as [string, Indicator][]
]);