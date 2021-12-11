import java.io.File

fun String.permute(result: String = ""): List<String> =
    if (isEmpty()) listOf(result) else flatMapIndexed { i, c -> removeRange(i, i + 1).permute(result + c) }

val base = "abcdefg"
val allPermutations = base.permute()
val numbers = listOf("abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg")

fun String.translate(permutation: String) = map { base[permutation.indexOf(it)] }.sorted().joinToString("")

File("8.in").readLines().map { line ->
    val (scrambled, query) = line.split(" | ").map { it.split(" ") }
    val p = allPermutations.first { perm -> scrambled.map { it.translate(perm) }.toSet() == numbers.toSet() }
    query.map { numbers.indexOf(it.translate(p)) }.joinToString("").toInt()
}.sum()
