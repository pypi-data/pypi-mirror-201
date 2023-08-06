import unittest
from arrendatools_modelo_303.modelo_303 import Modelo303
from arrendatools_modelo_303.periodos import Periodo


class Modelo303TestCase(unittest.TestCase):

    def test_generar_modelo_123T_cuota_positiva(self):
        expected_result = "<T303020231T0000><AUX>                                                                      v1.0    12345678X                                                                                                                                                                                                                     </AUX><T30301000> U12345678EDE LOS PALOTES PERICO                                                           20231T22322222200000000 20000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000005000000000000000000000000000000000000010000000000000000000000000000000200000021000000000000004200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001750000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000005200000000000000000000000000000000000000000000000000000000000000004200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000042000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     </T30301000><T30303000>0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000420001000000000000000042000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000042000000000000000000000000000000000000000000000000042000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       </T30303000><T303DID00>           ES0012341234123412341234                                                                                                                                                   0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         </T303DID00></T303020231T0000>"
        periodo = Periodo.P1T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678E"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.00
        gastos_bienes_servicios = 0.0
        iva_gastos_bienes_servicios = 0.0
        adquisiciones_bienes_inversion = 0.0
        iva_adquisiciones_bienes_inversion = 0.0
        volumen_anual_operaciones = None

        datos_modelo = Modelo303(
            periodo=periodo,
            nif_empresa_desarrollo=nif_empresa_desarrollo,
            version=version,
            nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
            nif_contribuyente=nif_contribuyente,
            iban=iban,
            base_imponible=base_imponible,
            gastos_bienes_servicios=gastos_bienes_servicios,
            iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
            adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
            iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
            volumen_anual_operaciones=volumen_anual_operaciones
        )

        datos_fichero = datos_modelo.generar()
        self.assertEquals(datos_fichero, expected_result)

    def test_generar_modelo_123T_cuota_negativa(self):
        expected_result = "<T303020231T0000><AUX>                                                                      v1.0    12345678X                                                                                                                                                                                                                     </AUX><T30301000> C12345678EDE LOS PALOTES PERICO                                                           20231T22322222200000000 200000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000050000000000000000000000000000000000000100000000000000000000000000000002000000210000000000000042000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000017500000000000000000000000000000000000000000000000000000000000000000000000000014000000000000000000000000000000000000052000000000000000000000000000000000000000000000000000000000000000042000000000000002500000000000000005250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000052500N0000000000010500                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     </T30301000><T30303000>0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000N000000000001050010000N00000000000105000000000000000000000000000000000000000000000000000000000000000000000000000000000000000N00000000000105000000000000000000000000000000000000N0000000000010500                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       </T30303000><T303DID00>                                                                                                                                                                                      0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         </T303DID00></T303020231T0000>"
        periodo = Periodo.P1T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678E"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.00
        gastos_bienes_servicios = 2500.0
        iva_gastos_bienes_servicios = 525.0
        adquisiciones_bienes_inversion = 0.0
        iva_adquisiciones_bienes_inversion = 0.0
        volumen_anual_operaciones = None

        datos_modelo = Modelo303(
            periodo=periodo,
            nif_empresa_desarrollo=nif_empresa_desarrollo,
            version=version,
            nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
            nif_contribuyente=nif_contribuyente,
            iban=iban,
            base_imponible=base_imponible,
            gastos_bienes_servicios=gastos_bienes_servicios,
            iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
            adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
            iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
            volumen_anual_operaciones=volumen_anual_operaciones
        )

        datos_fichero = datos_modelo.generar()
        self.assertEquals(datos_fichero, expected_result)

    def test_generar_modelo_4T_cuota_positiva(self):
        expected_result = "<T303020234T0000><AUX>                                                                      v1.0    12345678X                                                                                                                                                                                                                     </AUX><T30301000> U12345678EDE LOS PALOTES PERICO                                                           20234T22322222200000000 21100000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000005000000000000000000000000000000000000010000000000000000000000000000000200000021000000000000004200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001750000000000000000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000005200000000000000000000000000000000000000000000000000000000000000004200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000042000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     </T30301000><T30303000>0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000420001000000000000000042000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000042000000000000000000000000000000000000000000000000042000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       </T30303000><T30304000> A018612                                    0000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        </T30304000><T30305000>    0000000000000000000000000000000000 00000   0000000000000000000000000000000000 00000   0000000000000000000000000000000000 00000   0000000000000000000000000000000000 00000   0000000000000000000000000000000000 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                </T30305000><T303DID00>           ES0012341234123412341234                                                                                                                                                   0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         </T303DID00></T303020234T0000>"
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678E"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.00
        gastos_bienes_servicios = 0.0
        iva_gastos_bienes_servicios = 0.0
        adquisiciones_bienes_inversion = 0.0
        iva_adquisiciones_bienes_inversion = 0.0
        volumen_anual_operaciones = 6000.0

        datos_modelo = Modelo303(
            periodo=periodo,
            nif_empresa_desarrollo=nif_empresa_desarrollo,
            version=version,
            nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
            nif_contribuyente=nif_contribuyente,
            iban=iban,
            base_imponible=base_imponible,
            gastos_bienes_servicios=gastos_bienes_servicios,
            iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
            adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
            iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
            volumen_anual_operaciones=volumen_anual_operaciones
        )

        datos_fichero = datos_modelo.generar()
        self.assertEquals(datos_fichero, expected_result)

    def test_generar_modelo_4T_cuota_negativa(self):
        self.assertTrue(True)

    def test_generar_modelo_4T_volumen_anual_None(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678X"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = None

        with self.assertRaisesRegex(ValueError, "El volumen anual de operaciones es obligatorio en el 4º trimestre*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_nif_ed_largo(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678XXXXXXXXXXXXXXXXXXXXXXX"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678X"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "El NIF de la empresa de desarrollo debe ser de*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_nif_ed_corto(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678X"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "El NIF de la empresa de desarrollo debe ser de*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_nif_contribuyente_largo(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678XXXXXXXXXXXXXXXXXXXXXXX"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "El NIF del contribuyente debe ser de*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_nif_contribuyente_corto(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "El NIF del contribuyente debe ser de*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_version_largo(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.123"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "La versión no puede tener más de *"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_nombre_largo(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO PERO QUE SEA MAYOR DE LO PERMITIDO POR LA AGENCIA TRIBUTARIA"
        nif_contribuyente = "12345678X"
        iban = "ES0012341234123412341234"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "El nombre o razón social del contribuyente no puede tener más de*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )

    def test_generar_modelo_iban_largo(self):
        periodo = Periodo.P4T
        nif_empresa_desarrollo = "12345678X"
        version = "v1.0"
        nombre_fiscal_contribuyente = "DE LOS PALOTES PERICO"
        nif_contribuyente = "12345678X"
        iban = "ES001234123412341234123412345678901"
        base_imponible = 2000.0
        gastos_bienes_servicios = 1000.0
        iva_gastos_bienes_servicios = 210.0
        adquisiciones_bienes_inversion = 2000.0
        iva_adquisiciones_bienes_inversion = 420.0
        volumen_anual_operaciones = 6000.00

        with self.assertRaisesRegex(ValueError, "El IBAN no puede tener más de*"):
            Modelo303(
                periodo=periodo,
                nif_empresa_desarrollo=nif_empresa_desarrollo,
                version=version,
                nombre_fiscal_contribuyente=nombre_fiscal_contribuyente,
                nif_contribuyente=nif_contribuyente,
                iban=iban,
                base_imponible=base_imponible,
                gastos_bienes_servicios=gastos_bienes_servicios,
                iva_gastos_bienes_servicios=iva_gastos_bienes_servicios,
                adquisiciones_bienes_inversion=adquisiciones_bienes_inversion,
                iva_adquisiciones_bienes_inversion=iva_adquisiciones_bienes_inversion,
                volumen_anual_operaciones=volumen_anual_operaciones
            )


if __name__ == '__main__':
    unittest.main()
