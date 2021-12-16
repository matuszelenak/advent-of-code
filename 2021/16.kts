import java.io.File
import java.math.BigInteger

sealed class Packet(
    open val version: Int,
    open val type: Int
) {
    abstract fun evaluate(): BigInteger

    data class LiteralPacket(
        override val version: Int,
        override val type: Int,
        val value: BigInteger
    ) : Packet(version, type) {
        override fun evaluate(): BigInteger = value
    }

    data class OperatorPacket(
        override val version: Int,
        override val type: Int,
        val operands: List<Packet>
    ) : Packet(version, type) {
        override fun evaluate(): BigInteger = when (type) {
            0 -> operands.sumOf { it.evaluate() }
            1 -> operands.map { it.evaluate() }.fold(BigInteger.ONE, BigInteger::times)
            2 -> operands.minOf { it.evaluate() }
            3 -> operands.maxOf { it.evaluate() }
            5 -> if (operands[0].evaluate() > operands[1].evaluate()) BigInteger.ONE else BigInteger.ZERO
            6 -> if (operands[0].evaluate() < operands[1].evaluate()) BigInteger.ONE else BigInteger.ZERO
            7 -> if (operands[0].evaluate() == operands[1].evaluate()) BigInteger.ONE else BigInteger.ZERO
            else -> throw IllegalArgumentException()
        }
    }
}

fun Packet.sumVersions(): Int = when (this) {
    is Packet.LiteralPacket -> version
    is Packet.OperatorPacket -> version + operands.sumOf { it.sumVersions() }
}

fun String.hexToBin() = map { Integer.toBinaryString(it.toString().toInt(16)).padStart(4, '0') }.joinToString("")

fun <T> Iterator<T>.read(length: Int): String = (1..length).map { next() }.joinToString("")
fun <T> Iterator<T>.readInt(length: Int): Int = read(length).toInt(2)

fun Iterator<Char>.readNPackets(n: Int): Pair<List<Packet>, Int> {
    return (1..n).map {
        parsePacket()
    }.let { list ->
        list.map { it.first } to list.sumOf { it.second }
    }
}

fun Iterator<Char>.readPacketsOfLength(length: Int): Pair<List<Packet>, Int> {
    var totalRead = 0
    val packets = mutableListOf<Packet>()
    do {
        val (packet, packetLength) = parsePacket()
        packets.add(packet)
        totalRead += packetLength
    } while (totalRead < length)

    return packets to totalRead
}

fun Iterator<Char>.parsePacket(): Pair<Packet, Int> {
    val version = readInt(3)
    val type = readInt(3)

    var totalRead = 6
    return if (type == 4) {
        val value = mutableListOf<String>()
        while (true) {
            val chunk = read(5)
            totalRead += 5
            value.add(chunk.drop(1))
            if (chunk.first() == '0') {
                break
            }
        }
        Packet.LiteralPacket(version, type, value.joinToString("").toBigIntegerOrNull(2)!!)
    } else {
        val lengthTypeId = readInt(1)
        totalRead++

        val (packets, packetsLength) = if (lengthTypeId == 0) {
            val length = readInt(15)
            totalRead += 15
            readPacketsOfLength(length)
        } else {
            val number = readInt(11)
            totalRead += 11
            readNPackets(number)
        }
        totalRead += packetsLength

        Packet.OperatorPacket(version, type, packets)
    }.let {
        it to totalRead
    }
}

val bin = File("16.in").readLines().first().hexToBin()
val packet = bin.iterator().parsePacket().first

packet.evaluate()