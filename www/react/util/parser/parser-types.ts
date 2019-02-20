
export interface Indicator {
    kind: string
}

export class Price implements Indicator {
    readonly kind = "currentprice";

    constructor() {}

}

export class SMA implements Indicator {
    readonly kind = "sma";

    constructor(public period: number) {}

}

export class EMA implements Indicator {
    readonly kind = "ema";

    constructor(public period: number) {}

}

export class RSI implements Indicator {
    readonly kind = "rsi";

    constructor(public period: number) {}

}

export class RealNum implements Indicator {
    readonly kind = "real";

    constructor(public val: number) {}
}


export type Exp = Eq | LT | GT | LEq | GEq | And | Or | Not;

export class Eq {
    readonly kind = "Eq";

    constructor(public l: Indicator, public r: Indicator) {}
}

export class LT {
    readonly kind = "LT";

    constructor(public l: Indicator, public r: Indicator) {}
}

export class GT {
    readonly kind = "GT";

    constructor(public l: Indicator, public r: Indicator) {}
}

export class LEq {
    readonly kind = "LEq";

    constructor(public l: Indicator, public r: Indicator) {}
}

export class GEq {
    readonly kind = "GEq";

    constructor(public l: Indicator, public r: Indicator) {}
}

export class And {
    readonly kind = "And";

    constructor(public e1: Exp, public e2: Exp) {}
}

export class Or {
    readonly kind = "Or";

    constructor(public e1: Exp, public e2: Exp) {}
}

export class Not {
    readonly kind = "Not";

    constructor(public e: Exp) {}
}