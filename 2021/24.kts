val params = listOf(
    Triple(11, 8, 1),
    Triple(12, 8, 1),
    Triple(10, 12, 1),
    Triple(-8, 10, 26),
    Triple(15, 2, 1),
    Triple(15, 8, 1),
    Triple(-11, 4, 26),
    Triple(10, 9, 1),
    Triple(-3, 10, 26),
    Triple(15, 3, 1),
    Triple(-3, 7, 26),
    Triple(-1, 7, 26),
    Triple(-10, 2, 26),
    Triple(-16, 2, 26)
)

fun Int.nextZ(input: Int, firstParam: Int, secondParam: Int, divisor: Int): Int {
    val x = this.mod(26) + firstParam
    val nextZ = this.div(divisor)
    return if (x != input) {
        nextZ * 26 + input + secondParam
    } else {
        nextZ
    }
}

var acc = ""

fun Int.evolve(afterSteps: Int, cache: MutableMap<Pair<Int, Int>, Boolean>): Boolean {
    return cache[this to afterSteps] ?: if (afterSteps == params.size) {
        this == 0
    } else {
        val (first, second, divisor) = params[afterSteps]

        (9 downTo 1).firstOrNull { digit ->
            nextZ(digit, first, second, divisor).evolve(afterSteps + 1, cache)
        }?.let { winningDigit ->
            acc = "$winningDigit$acc"
            true
        } ?: false
    }.also { cache[this to afterSteps] = it }
}

0.evolve(0, mutableMapOf())

acc