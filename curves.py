from curve import EllipticCurve

curves = {
    'secp160r2': EllipticCurve( # see http://www.secg.org/SEC2-Ver-1.0.pdf, pg 11
        name = 'secp160r2',
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC73,
        a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC70,
        b = 0xB4E134D3FB59EB8BAB57274904664D5AF50388BA,
        g = (
            0x52DCB034293A117E1F4FF11B30F7199D3144CE6D,
            0xFEAFFEF2E331F296E071FA0DF9982CFEA7D43F2E
        ),
        n = 0x00000000000000000000351EE786A818F3A1A16B,
        h = 1
    )
}
