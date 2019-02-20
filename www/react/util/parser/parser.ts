import * as P from 'parsimmon';
import * as Type from './parser-types';


/** Begin combinator definitions **/
const token = (parser) => parser.skip(P.optWhitespace);

const Integer = (): P.Parser<number> => {
    return P.regexp(/([+-]?[1-9]\d*|0)/).thru(token);
};

const Real = (): P.Parser<number> => {
    return P.regexp(/-?\d+(\.\d*)?/).thru(token);
};

const indicator = (): P.Parser<Type.Indicator> => {
    return P.alt(
        Real().map(r => new Type.RealNum(r)),
        P.string("current-price").thru(token).map(_ => new Type.Price()),
        P.seq(P.string("sma").thru(token), P.string("(").thru(token), Integer(), P.string(")").thru(token))
            .map(([_1, _2, period, _3]) => new Type.SMA(period)),
        P.seq(P.string("ema").thru(token), P.string("(").thru(token), Integer(), P.string(")").thru(token))
            .map(([_1, _2, period, _3]) => new Type.EMA(period)),
        P.seq(P.string("rsi").thru(token), P.string("(").thru(token), Integer(), P.string(")").thru(token))
            .map(([_1, _2, period, _3]) => new Type.RSI(period))

    );
};

const atom = P.lazy((): P.Parser<Type.Exp> => {
    return P.alt(
        P.seq(indicator(), P.string("=").thru(token), indicator()).map(([l, _, r]) => new Type.Eq(l, r) as Type.Exp),
        P.seq(indicator(), P.string(">").thru(token), indicator()).map(([l, _, r]) => new Type.GT(l, r) as Type.Exp),
        P.seq(indicator(), P.string("<").thru(token), indicator()).map(([l, _, r]) => new Type.LT(l, r) as Type.Exp),
        P.seq(indicator(), P.string(">=").thru(token), indicator()).map(([l, _, r]) => new Type.GEq(l, r) as Type.Exp),
        P.seq(indicator(), P.string("<=").thru(token), indicator()).map(([l, _, r]) => new Type.LEq(l, r) as Type.Exp),
        P.seq(indicator(), P.string("!=").thru(token), indicator()).map(([l, _, r]) => new Type.Not(new Type.Eq(l, r) as Type.Exp)),
        P.seq(P.string("(").thru(token), exp, P.string(")").thru(token)).map(([_1, e, _2]) => e),
        P.seq(P.string("!").thru(token), P.string("(").thru(token), exp, P.string(")").thru(token)).map(([_1, _2, e, _3]) => new Type.Not(e) as Type.Exp)
    );
});

const and = P.lazy((): P.Parser<Type.Exp> => {
    return P.alt(
        P.seq(atom, P.string("&&").thru(token).then(and)).map(([e1, e2]) => new Type.And(e1, e2) as Type.Exp),
        atom
    );
});

const or = P.lazy((): P.Parser<Type.Exp> => {
    return P.alt(
        P.seq(and, P.string("||").thru(token).then(or)).map(([e1, e2]) => new Type.Or(e1, e2) as Type.Exp),
        and
    );
});

const exp = P.lazy(() => or);

/**
 * The meat of the parser combinator. Evaluates an expression and returns a list of all the indicators required
 * to process the condition query.typesc
 *
 * @param {Type.Exp} e The expression to be evaluated
 */
export const evaluateIndicators = (e: Type.Exp): string[] => {
    switch (e.kind) {
        case "Eq":
        case "LT":
        case "GT":
        case "LEq":
        case "GEq":
            let indicators = [];
            if (e.l instanceof Type.SMA || e.l instanceof Type.EMA || e.l instanceof Type.RSI) {
                indicators.push(`${e.l.kind}-${e.l.period}`);
            }

            if (e.r instanceof Type.SMA || e.r instanceof Type.EMA || e.r instanceof Type.RSI) {
                indicators.push(`${e.r.kind}-${e.r.period}`);
            }
            // TODO(jbartola): Add support for bollinger bands and MACD
            return indicators;

        case "And":
        case "Or": return evaluateIndicators(e.e1).concat(evaluateIndicators(e.e2));
        case "Not": return evaluateIndicators(e.e);
    }

    return [];
};

/**
 * Parses a string using the condition parser. Returns an Exp if the query parses, otherwise
 * returns undefined
 *
 * @param str
 */
export const parse = (str: string): Type.Exp | undefined => {
    const trimmed = str.trim();
    let result;

    try {
        result = exp.tryParse(trimmed);
        console.log(result);
    } catch (err) {
        // console.log(err);
    }

    return result;
};