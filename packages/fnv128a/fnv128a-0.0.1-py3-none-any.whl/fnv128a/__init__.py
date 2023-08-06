from typing import Tuple

# Based on https://cs.opensource.google/go/go/+/refs/tags/go1.20.3:src/hash/fnv/fnv.go;l=30
OFFSET_LOWER = 0x62b821756295c58d # 7113472399480571277
OFFSET_HIGHER =  0x6c62272e07bb0142 # 7809847782465536322
PRIMER_LOWER = 0x13b
PRIME_SHIFT = 24
 
MASK32 = (1 << 32) - 1
MASK64 = (1 << 64) - 1


def mul64(x: int, y: int) -> Tuple[int, int]:
    """
    Based on https://pkg.go.dev/math/bits#Mul64 implementation below:
    ```
    func Mul64(x, y uint64) (hi, lo uint64) {
        const mask32 = 1<<32 - 1
        x0 := x & mask32
        x1 := x >> 32
        y0 := y & mask32
        y1 := y >> 32
        w0 := x0 * y0
        t := x1*y0 + w0>>32
        w1 := t & mask32
        w2 := t >> 32
        w1 += x0 * y1
        hi = x1*y1 + w2 + w1>>32
        lo = x * y
        return
    }
    ```
    We aggressively mask any expansive operations to replicate Go uint64 overflow behavior.
    """
    x0 = x & MASK32
    x1 = x >> 32
    y0 = y & MASK32
    y1 = y >> 32
    w0 = (x0 * y0) & MASK64
    t = (x1 * y0 + (w0 >> 32)) & MASK64
    w1 = t & MASK32
    w2 = t >> 32
    w1 += (x0 * y1) & MASK64
    hi = (x1*y1 + w2 + (w1 >> 32)) & MASK64
    lo = (x * y) & MASK64
    return hi, lo


def compute_fnv128a(data: bytes) -> bytes:
    """
    Python re-implementation of https://pkg.go.dev/hash/fnv#New128a;
    see derived implementation below.
    ```
    func (s *sum128a) Write(data []byte) (int, error) {
        for _, c := range data {
            s[1] ^= uint64(c)
            // Compute the multiplication
            s0, s1 := bits.Mul64(prime128Lower, s[1])
            s0 += s[1]<<prime128Shift + prime128Lower*s[0]
            // Update the values
            s[1] = s1
            s[0] = s0
        }
        return len(data), nil
    }
    ```
    Likewise, we aggressively mask any expansive operations to replicate Go uint64 overflow behavior.
    """
    s = [OFFSET_HIGHER, OFFSET_LOWER]

    # sum128a.Write
    for bs in data:
        s[1] = (s[1]^bs) & MASK64
        s0, s1 = mul64(PRIMER_LOWER, s[1])
        s0 += ((s[1] << PRIME_SHIFT) + PRIMER_LOWER * s[0]) & MASK64
        s[1], s[0] = s1, s0

    # sum128a.Sum
    byte_array = []
    for bound in s:
        for shift in [56, 48, 40, 32, 24, 16, 8, 0]:
            # Golang uint64 -> byte overflows
            byte = (bound >> shift) % 256
            byte_array.append(byte)

    return bytes(byte_array)


bytes_array = compute_fnv128a(b'itemsFeatures')
target =  b"\xeeb\xab\xb2\xe0S\xbd\xdd\xc8\t\xfba\xd6\xf7\xdah"
assert bytes_array == target