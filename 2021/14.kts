import java.io.File
import java.math.BigDecimal

File("14.in").readLines().let { content ->
    val template = content.first()
    val rules = content.drop(2).associate { rule ->
        val (from, to) = rule.split(" -> ")
        from to to.first()
    }

    val pairs = mutableMapOf<Pair<Char, Char>, BigDecimal>().withDefault { BigDecimal.ZERO }
    template.zipWithNext { a, b -> pairs[a to b] = pairs.getValue(a to b) + BigDecimal.ONE }

    repeat(100) {
        val deltas = pairs.keys.associateWith { BigDecimal.ZERO }.toMutableMap().withDefault { BigDecimal.ZERO }

        pairs.entries.forEach { (pair, count) ->
            rules["${pair.first}${pair.second}"]?.let { newEntry ->
                deltas[pair.first to newEntry] = deltas.getValue(pair.first to newEntry) + count
                deltas[newEntry to pair.second] = deltas.getValue(newEntry to pair.second) + count
                deltas[pair.first to pair.second] = deltas.getValue(pair.first to pair.second) - count
            }
        }
        deltas.entries.forEach { (pair, delta) ->
            pairs[pair] = pairs.getValue(pair) + delta
        }
    }

    val letterCounts = mapOf(template.first() to BigDecimal.ONE, template.last() to BigDecimal.ONE)
        .toMutableMap().withDefault { BigDecimal.ZERO }
    pairs.entries.forEach { (pair, count) ->
        letterCounts[pair.first] = letterCounts.getValue(pair.first) + count
        letterCounts[pair.second] = letterCounts.getValue(pair.second) + count
    }

    val min = letterCounts.values.minOrNull()!!.divide(2.0.toBigDecimal())
    val max = letterCounts.values.maxOrNull()!!.divide(2.0.toBigDecimal())
    println(max - min)
}