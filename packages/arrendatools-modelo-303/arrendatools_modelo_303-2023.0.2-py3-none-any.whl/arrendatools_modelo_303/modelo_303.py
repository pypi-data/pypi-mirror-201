from arrendatools_modelo_303.periodos import Periodo


class Modelo303:
    """Clase que contiene los datos necesarios para generar el modelo 303 trimestral para arrendadores con IVA.

    Attributes:
        periodo (string): Periodo de la declaración Datos validos: (1T, 2T, 3T o 4T)
        nif_empresa_desarrollo (string): NIF de la empresa de desarrollo. A cumplimentar por las entidades desarrolladoras (EEDD). Máximo 9 caracteres.
        version (string): Versión del programa. Debe consignarse el identificador de la versión del SW desarrollado por la ED. Máximo 4 caracteres.
        nombre_fiscal (string): Apellidos y nombre o Razón social del contribuyente. Máximo 80 caracteres.
        nif_contribuyente: (string): NIF contribuyente. Máximo 9 caracteres.
        iban (string): IBAN donde domiciliar el pago/devolucion.
        base_impobible (float): Importe trimestral del alquiler sin computar el IVA. Tenga en cuenta que la base imponible del IVA en el arrendamiento de un local de negocio está constituida por el importe total de la contraprestación, incluyendo no solo el importe de la renta, sino también las cantidades asimiladas que el arrendador pueda exigir al arrendatario o inquilino. Por ejemplo, los gastos de comunidad, el IBI, los gastos de suministros (calefacción, agua, luz), las reparaciones y otros conceptos análogos. En ocasiones, estos gastos son facturados al arrendador y posteriormente el arrendador los repercute al arrendatario. No se solicitan las cuotas de IVA puesto que se calculan aplicando sobre la base consignada el 21 por 100. Tenga en cuenta que deberá declarar las cuotas de arrendamiento exigibles, hayan sido cobradas o no. En caso de impago podrá recuperar el IVA ingresado cuando se cumplan los requisitos previstos en el artículo 80.Tres o Cuatro, consignando las casillas "Modificación bases y cuotas" (casillas 14 y 15).
        gastos_bienes_servicios (float): Base imponible trimestral de los gastos en bienes y servicios corrientes.
        iva_gastos_bienes_servicios (float): IVA trimestral soportado deducible de los gastos en bienes y servicios corrientes. Para ser deducible el IVA soportado debe disponer de factura completa emitida a nombre del arrendador. Podrá incluir, entre otras, las cuotas soportadas por suministros, reparaciones y obras de mejora, servicios profesionales independientes (abogados, asesoría, notaría, API) y servicios exteriores (publicidad, limpieza, vigilancia). No son deducibles, ni siquiera parcialmente, las cuotas soportadas en bienes y servicios que se utilicen simultáneamente para esta actividad y para necesidades privadas cuando el precio de adquisición sea inferior a 3.005,06 euros (ordenadores, móviles...). Tampoco son deducibles los gastos en los que no se soporte el impuesto (intereses de préstamo, seguros, IBI o la amortización del inmueble).
        adquisiciones_bienes_inversion (float): Base imponible trimestral de las adquisiciones de bienes de inversión.
        iva_adquisiciones_bienes_inversion (float): IVA trimestral soportado deducible de las adquisiciones de bienes de inversión. Podrá deducir el importe de las cuotas soportadas por la adquisición de bienes de inversión (cuantía superior a 3.005,06 euros) que se utilicen en la actividad de arrendamiento, como el mobiliario. Asimismo, el IVA soportado en la construcción o adquisición del inmueble, las obras de reforma o mejoras. En el caso de que la afectación a la actividad sea parcial, deberá calcularse la parte afecta.
        volumen_anual_operaciones (float): Volumen anual de operaciones. Sólo necesario para 4T.
    """
    _LONGITUD_NIF = 9

    _MAX_LONGITUD_IBAN = 34
    _MAX_LONGITUD_VERSION = 4
    _MAX_LONGITUD_NOMBRE_FISCAL_CONTRIBUYENTE = 80
    _EJERCICIO = "2023"

    _INICIO_APERTURA = "<T"
    _INICIO_CIERRE = "</T"
    _MODELO = "303"
    _DISCRIMINANTE = "0"
    _CIERRE = ">"
    _TIPO_Y_CIERRE = "0000" + _CIERRE
    _AUX_APERTURA = "<AUX>"
    _AUX_CIERRE = "</AUX>"
    _RESERVADO_ADMON_4_ESPACIOS = "".ljust(4, ' ')      # 4 espacios
    _RESERVADO_ADMON_13_ESPACIOS = "".ljust(13, ' ')    # 13 espacios
    _RESERVADO_ADMON_35_ESPACIOS = "".ljust(35, ' ')    # 35 espacios
    _RESERVADO_ADMON_70_ESPACIOS = "".ljust(70, ' ')    # 70 espacios
    _RESERVADO_ADMON_86_ESPACIOS = "".ljust(86, ' ')    # 86 espacios
    _RESERVADO_ADMON_200_ESPACIOS = "".ljust(200, ' ')  # 200 espacios
    _RESERVADO_ADMON_213_ESPACIOS = "".ljust(213, ' ')  # 213 espacios
    _RESERVADO_ADMON_479_ESPACIOS = "".ljust(479, ' ')  # 479 espacios
    _RESERVADO_ADMON_600_ESPACIOS = "".ljust(600, ' ')  # 600 espacios
    _RESERVADO_ADMON_617_ESPACIOS = "".ljust(617, ' ')  # 617 espacios
    _RESERVADO_ADMON_672_ESPACIOS = "".ljust(672, ' ')  # 672 espacios
    _DP30301 = "01000"
    _DP30302 = "02000"
    _DP30303 = "03000"
    _DP30304 = "04000"
    _DP30305 = "05000"
    _DP303DID = "DID00"
    _DP30301_APERTURA = _INICIO_APERTURA + _MODELO + _DP30301 + _CIERRE
    _DP30301_CIERRE = _INICIO_CIERRE + _MODELO + _DP30301 + _CIERRE
    # _DP30302_APERTURA = _INICIO_APERTURA + _MODELO + _DP30302 + _CIERRE
    # _DP30302_CIERRE = _INICIO_CIERRE + _MODELO + _DP30302 + _CIERRE
    _DP30303_APERTURA = _INICIO_APERTURA + _MODELO + _DP30303 + _CIERRE
    _DP30303_CIERRE = _INICIO_CIERRE + _MODELO + _DP30303 + _CIERRE
    _DP30304_APERTURA = _INICIO_APERTURA + _MODELO + _DP30304 + _CIERRE
    _DP30304_CIERRE = _INICIO_CIERRE + _MODELO + _DP30304 + _CIERRE
    _DP30305_APERTURA = _INICIO_APERTURA + _MODELO + _DP30305 + _CIERRE
    _DP30305_CIERRE = _INICIO_CIERRE + _MODELO + _DP30305 + _CIERRE
    _DP303DID_APERTURA = _INICIO_APERTURA + _MODELO + _DP303DID + _CIERRE
    _DP303DID_CIERRE = _INICIO_CIERRE + _MODELO + _DP303DID + _CIERRE
    _PAGINA_COMPLEMENTARIA_ESPACIO = " "
    _NO_ES_4T = "0"
    _SI = "1"
    _NO = "2"
    _NO_SOLO_RG = "3"

    def __init__(
        self,
        periodo,                                 # Periodo de la declaración Datos validos: (1T, 2T, 3T o 4T)
        nif_empresa_desarrollo,                  # NIF de la empresa de desarrollo. A cumplimentar por las entidades desarrolladoras (EEDD). Máximo 9 caracteres.
        version,                                 # Versión del programa: Debe consignarse el identificador de la versión del SW desarrollado por la ED. Máximo 4 caracteres.
        nombre_fiscal_contribuyente,             # Apellidos y nombre o Razón social del contribuyente. Máximo 80 caracteres.
        nif_contribuyente,                       # NIF contribuyente. Máximo 9 caracteres.
        iban,                                    # IBAN donde domiciliar el pago/devolucion.
        base_imponible,                          # Importe trimestral del alquiler sin computar el IVA. Tenga en cuenta que la base imponible del IVA en el arrendamiento de un local de negocio está constituida por el importe total de la contraprestación, incluyendo no solo el importe de la renta, sino también las cantidades asimiladas que el arrendador pueda exigir al arrendatario o inquilino. Por ejemplo, los gastos de comunidad, el IBI, los gastos de suministros (calefacción, agua, luz), las reparaciones y otros conceptos análogos. En ocasiones, estos gastos son facturados al arrendador y posteriormente el arrendador los repercute al arrendatario. No se solicitan las cuotas de IVA puesto que se calculan aplicando sobre la base consignada el 21 por 100. Tenga en cuenta que deberá declarar las cuotas de arrendamiento exigibles, hayan sido cobradas o no. En caso de impago podrá recuperar el IVA ingresado cuando se cumplan los requisitos previstos en el artículo 80.Tres o Cuatro, consignando las casillas "Modificación bases y cuotas" (casillas 14 y 15).
        gastos_bienes_servicios=0.0,             # Base imponible trimestral de los gastos en bienes y servicios corrientes.
        iva_gastos_bienes_servicios=0.0,         # IVA trimestral soportado deducible de los gastos en bienes y servicios corrientes. Para ser deducible el IVA soportado debe disponer de factura completa emitida a nombre del arrendador. Podrá incluir, entre otras, las cuotas soportadas por suministros, reparaciones y obras de mejora, servicios profesionales independientes (abogados, asesoría, notaría, API) y servicios exteriores (publicidad, limpieza, vigilancia). No son deducibles, ni siquiera parcialmente, las cuotas soportadas en bienes y servicios que se utilicen simultáneamente para esta actividad y para necesidades privadas cuando el precio de adquisición sea inferior a 3.005,06 euros (ordenadores, móviles...). Tampoco son deducibles los gastos en los que no se soporte el impuesto (intereses de préstamo, seguros, IBI o la amortización del inmueble).
        adquisiciones_bienes_inversion=0.0,      # Base imponible trimestral de las adquisiciones de bienes de inversión.
        iva_adquisiciones_bienes_inversion=0.0,  # IVA trimestral soportado deducible de las adquisiciones de bienes de inversión. Podrá deducir el importe de las cuotas soportadas por la adquisición de bienes de inversión (cuantía superior a 3.005,06 euros) que se utilicen en la actividad de arrendamiento, como el mobiliario. Asimismo, el IVA soportado en la construcción o adquisición del inmueble, las obras de reforma o mejoras. En el caso de que la afectación a la actividad sea parcial, deberá calcularse la parte afecta.
        volumen_anual_operaciones=0.0            # Volumen anual de operaciones. Sólo necesario para 4T.
    ):
        if len(nif_empresa_desarrollo) != Modelo303._LONGITUD_NIF:
            raise ValueError(f"El NIF de la empresa de desarrollo debe ser de {Modelo303._LONGITUD_NIF} caracteres")
        if len(version) > Modelo303._MAX_LONGITUD_VERSION:
            raise ValueError(f"La versión no puede tener más de {Modelo303._MAX_LONGITUD_VERSION} caracteres")
        if len(nombre_fiscal_contribuyente) > Modelo303._MAX_LONGITUD_NOMBRE_FISCAL_CONTRIBUYENTE:
            raise ValueError(f"El nombre o razón social del contribuyente no puede tener más de {Modelo303._MAX_LONGITUD_NOMBRE_FISCAL_CONTRIBUYENTE} caracteres")
        if len(nif_contribuyente) != Modelo303._LONGITUD_NIF:
            raise ValueError(f"El NIF del contribuyente debe ser de {Modelo303._LONGITUD_NIF} caracteres")
        if len(iban) > Modelo303._MAX_LONGITUD_IBAN:
            raise ValueError(f"El IBAN no puede tener más de {Modelo303._MAX_LONGITUD_IBAN} caracteres")
        if (periodo == Periodo.P4T and volumen_anual_operaciones is None):
            raise ValueError("El volumen anual de operaciones es obligatorio en el 4º trimestre (4T)")

        self.ejercicio = self._EJERCICIO
        self.periodo = periodo.value
        self.nif_empresa_desarrollo = nif_empresa_desarrollo.upper()
        self.version = version
        self.nombre_fiscal = nombre_fiscal_contribuyente.upper()
        self.nif_contribuyente = nif_contribuyente.upper()
        self.iban = iban.upper()
        self.base_imponible = base_imponible
        if not gastos_bienes_servicios:
            self.gastos_bienes_servicios = 0.0
        else:
            self.gastos_bienes_servicios = gastos_bienes_servicios
        if not iva_gastos_bienes_servicios:
            self.iva_gastos_bienes_servicios = 0.0
        else:
            self.iva_gastos_bienes_servicios = iva_gastos_bienes_servicios
        if not adquisiciones_bienes_inversion:
            self.adquisiciones_bienes_inversion = 0.0
        else:
            self.adquisiciones_bienes_inversion = adquisiciones_bienes_inversion
        if not iva_adquisiciones_bienes_inversion:
            self.iva_adquisiciones_bienes_inversion = 0.0
        else:
            self.iva_adquisiciones_bienes_inversion = iva_adquisiciones_bienes_inversion
        self.volumen_anual_operaciones = volumen_anual_operaciones

    def generar(self):
        """
        Genera el string para la importación de datos en el modelo 303 de la Agencia Tributaria de España (PRE 303 - Servicio ayuda modelo 303).
        El string generado se puede guardar en un fichero y es compatible con el modelo 303 para la presentación trimestral del IVA.
        """

        REGISTRO_GENERAL_APERTURA = self._INICIO_APERTURA + self._MODELO + self._DISCRIMINANTE + self.ejercicio + self.periodo + self._TIPO_Y_CIERRE
        REGISTRO_GENERAL_CIERRE = self._INICIO_CIERRE + self._MODELO + self._DISCRIMINANTE + self.ejercicio + self.periodo + self._TIPO_Y_CIERRE
        datos = REGISTRO_GENERAL_APERTURA
        datos += self._generar_dp303_00()
        datos += self._generar_dp303_01()
        datos += self._generar_dp303_02()
        datos += self._generar_dp303_03()
        if (self.periodo == "4T"):
            datos += self._generar_dp303_04()
            datos += self._generar_dp303_05()
        datos += self._generar_dp303_did()
        datos += REGISTRO_GENERAL_CIERRE
        return datos

    def _generar_dp303_00(self):
        """
        Genera los datos de la seccion DP30300 del modelo 303.
        """

        datos = self._AUX_APERTURA
        datos += self._RESERVADO_ADMON_70_ESPACIOS
        datos += self.version
        datos += self._RESERVADO_ADMON_4_ESPACIOS
        datos += self.nif_empresa_desarrollo
        datos += self._RESERVADO_ADMON_213_ESPACIOS
        datos += self._AUX_CIERRE
        return datos

    def _generar_dp303_01(self):
        """
        Genera los datos de la seccion DP30301 del modelo 303.
        """

        iva_devengado = round(self.base_imponible * 0.21, 2)
        total_iva_deducible = round(self.iva_gastos_bienes_servicios + self.iva_adquisiciones_bienes_inversion, 2)
        cuota = self._calcula_couta()

        datos = self._DP30301_APERTURA  # Indicador de inicio de registro página 1
        datos += self._PAGINA_COMPLEMENTARIA_ESPACIO  # Indicador de página complementaria.
        datos += self._tipo_declaracion()  # Tipo Declaración
        datos += self.nif_contribuyente  # Identificación (1) - NIF
        datos += self.nombre_fiscal.ljust(80, ' ')  # Identificación (1) - Apellidos y nombre o Razón social
        datos += self.ejercicio  # Ejercicio
        datos += self.periodo  # Devengo
        datos += self._NO  # Identificación (1) - Tributación exclusivamente foral. Sujeto pasivo que tributa exclusivamente a una Administración tributaria Foral con IVA a la importación liquidado por la Aduana pendiente de ingreso
        datos += self._NO  # Identificación (1) - Sujeto pasivo inscrito en el Registro de devolución mensual (art. 30 RIVA)
        datos += self._NO_SOLO_RG  # Identificación (1) - Sujeto pasivo que tributa exclusivamente en régimen simplificado -> "1" SI (sólo RS), "2" NO (RG + RS), "3" NO (sólo RG).
        datos += self._NO  # Identificación (1) - Autoliquidación conjunta
        datos += self._NO  # Identificación (1) - Sujeto pasivo acogido al régimen especial del criterio de Caja (art. 163 undecies LIVA)
        datos += self._NO  # Identificación (1) - Sujeto pasivo destinatario de operaciones acogidas al régimen especial del criterio de caja
        datos += self._NO  # Identificación (1) - Opción por la aplicación de la prorrata especial (art. 103.Dos.1º LIVA)
        datos += self._NO  # Identificación (1) - Revocación de la opción por la aplicación de la prorrata especial
        datos += self._NO  # Identificación (1) - Sujeto pasivo declarado en concurso de acreedores en el presente período de liquidación
        datos += "".ljust(8, '0')  # Identificación (1) - Fecha en que se dictó el auto de declaración de concurso
        datos += "".ljust(1, ' ')  # Identificación (1) - Tipo de autoliquidación si se ha dictado auto de declaración de concurso en este período -> "1" SI Preconcursal, "2" SI postconcursal, blanco NO.
        datos += self._NO  # Identificación (1) - Sujeto pasivo acogido voluntariamente al SII
        datos += self._exoneracion_modelo_390(self.periodo)  # Identificación (1) - Sujeto pasivo exonerado de la Declaración-resumen anual del IVA, modelo 390
        datos += self._operaciones_distinto_0(self.periodo)  # Identificación (1) - Sujeto pasivo con volumen anual de operaciones distinto de cero (art. 121 LIVA)
        datos += self._base_tipo_cuota_str(0.0, 0.0, 0.0)  # IVA Devengado - Régimen general 0%. Casillas: [150], [151], [152]
        datos += self._base_tipo_cuota_str(0.0, 4.0, 0.0)  # IVA Devengado - Régimen general 4%. Casillas: [1], [2], [3]
        datos += self._base_tipo_cuota_str(0.0, 5.0, 0.0)  # IVA Devengado - Régimen general 5%. Casillas: [153], [154], [155]
        datos += self._base_tipo_cuota_str(0.0, 10.0, 0.0)  # IVA Devengado - Regimen general 10%. Casillas: [4], [5], [6]
        datos += self._base_tipo_cuota_str(self.base_imponible, 21.0, iva_devengado)  # IVA Devengado - Regimen general 21%. Casillas: [7], [8], [9]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Devengado - Adquisiciones intracomunitarias de bienes y servicios. Casillas: [10], [11]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Devengado - Otras operaciones con inversión del sujeto pasivo (excepto. adq. intracom). Casillas: [12], [13]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Devengado - Modificacion bases y cuotas. Casillas: [14], [15]
        datos += self._base_tipo_cuota_str(0.0, 1.75, 0.0)  # IVA Devengado - Recargo equivalencia 1,75%. Casillas: [156], [157], [158]
        datos += self._base_tipo_cuota_str(0.0, 0.0, 0.0)  # IVA Devengado - Recargo equivalencia 0%, 0,5% o 0,62%. Casillas: [16], [17], [18]
        datos += self._base_tipo_cuota_str(0.0, 1.4, 0.0)  # IVA Devengado - Recargo equivalencia 1,40%. Casillas: [19], [20], [21]
        datos += self._base_tipo_cuota_str(0.0, 5.2, 0.0)  # IVA Devengado - Recargo equivalencia 5,20%. Casillas: [22], [23], [24]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Devengado - Modificaciones bases y cuotas del recargo de equivalencia. Casillas: [25], [26]
        datos += self._convertir_a_centimos_str(iva_devengado)  # IVA Devengado - Total cuota devengada. Casillas: ( [152] + [03] + [155] + [06] + [09] + [11] + [13] + [15] + [158] + [18] + [21] + [24] + [26] ) [27]
        datos += self._base_cuota_str(self.gastos_bienes_servicios, self.iva_gastos_bienes_servicios)  # IVA Deducible - Por cuotas soportadas en operaciones interiores corrientes. Casillas: [28], [29]
        datos += self._base_cuota_str(self.adquisiciones_bienes_inversion, self.iva_adquisiciones_bienes_inversion)  # IVA Deducible - Por cuotas soportadas en operaciones interiores con bienes de inversión. Casillas: [30], [31]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Deducible - Por cuotas soportadas en las importaciones de bienes corrientes. Casillas: [32], [33]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Deducible - Por cuotas soportadas en las importaciones de bienes de inversión. Casillas: [34], [35]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Deducible - En adquisiciones intracomunitarias de bienes y servicios corrientes. Casillas: [36], [37]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Deducible - En adquisiciones intracomunitarias de bienes de inversión. Casillas: [38], [39]
        datos += self._base_cuota_str(0.0, 0.0)  # IVA Deducible - Rectificación de deducciones. Casillas: [40], [41]
        datos += self._convertir_a_centimos_str(0.0)  # IVA Deducible - Compensaciones Régimen Especial A.G. y P. Casillas: [42]
        datos += self._convertir_a_centimos_str(0.0)  # IVA Deducible - Regularización inversiones. Casillas: [43]
        datos += self._convertir_a_centimos_str(0.0)  # IVA Deducible - Regularización por aplicación del porcentaje definitivo de prorrata. Casillas: [44]
        datos += self._convertir_a_centimos_str(total_iva_deducible)  # IVA Deducible - Total a deducir. Casillas: ( [29] + [31] + [33] + [35] + [37] + [39] + [41] + [42] + [43] + [44] ) -> Cuota [45]
        datos += self._convertir_a_centimos_str(cuota)  # IVA Deducible - Resultado régimen general. Casillas: ( [27] - [45] ) -> Cuota [46]
        datos += self._RESERVADO_ADMON_600_ESPACIOS  # Reservado para la AEAT
        datos += self._RESERVADO_ADMON_13_ESPACIOS  # Reservado para la AEAT - Sello electrónico reservado para la AEAT
        datos += self._DP30301_CIERRE  # Indicador de fin de registro página 1
        return datos

    def _generar_dp303_02(self):
        """
        Genera los datos de la seccion DP30302 del modelo 303. En el caso de arrendadores con IVA esta sección no se tiene que rellenar.
        """

        return ""

    def _generar_dp303_03(self):
        """
        Genera los datos de la seccion DP30303 del modelo 303.
        """

        cuota = self._calcula_couta()

        resultado = cuota
        resultado_estado = cuota
        resultado_autoliquidacion = cuota
        resultado_final = cuota

        datos = self._DP30303_APERTURA
        datos += self._convertir_a_centimos_str(0.0)  # Información adicional - Entregas intracomunitarias de bienes y servicios. Casillas: [59]
        datos += self._convertir_a_centimos_str(0.0)  # Información adicional - Exportaciones y operaciones asimiladas. Casillas: [60]
        datos += self._convertir_a_centimos_str(0.0)  # Información adicional - Operaciones no sujetas por reglas de localización (excepto las incluidas en la casilla 123). Casillas: [120]
        datos += self._convertir_a_centimos_str(0.0)  # Información adicional - Operaciones sujetas con inversión del sujeto pasivo. Casillas: [122]
        datos += self._convertir_a_centimos_str(0.0)  # Información adicional - Operaciones no sujetas por reglas de localización acogidas a los regímenes especiales de ventanilla única. Casillas: [123]
        datos += self._convertir_a_centimos_str(0.0)  # Información adicional - Operaciones sujetas y acogidas a los regímenes especiales de ventanilla única. Casillas: [124]
        datos += self._base_cuota_str(0.0, 0.0)  # Información adicional - Importes de las entregas de bienes y prestaciones de servicios a las que habiéndoles sido aplicado el régimen especial del criterio de caja hubieran resultado devengadas conforme a la regla general de devengo contenida en el art. 75 LIVA. Casillas: [62], [63]
        datos += self._base_cuota_str(0.0, 0.0)  # Información adicional - Importes de las adquisiciones de bienes y servicios a las que sea de aplicación o afecte el régimen especial del criterio de caja. Casillas: [74], [75]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Regularización cuotas art. 80.cinco.5ª LIVA. Casillas: [76]
        datos += self._convertir_a_centimos_str(resultado)  # Resultado - Suma de resultados. Casillas: ( [46] + [58] + [76] ) [64]
        datos += self._porcentaje_str(100)  # Resultado - % Atribuible a la Administración del Estado. Casillas: [65]
        datos += self._convertir_a_centimos_str(resultado_estado)  # Resultado - Atribuible a la Administración del Estado. Casillas: [66]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - IVA a la importación liquidado por la Aduana pendiente de ingreso. Casillas: [77]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Cuotas a compensar pendientes de periodos anteriores. Casillas: [110]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Cuotas a compensar de periodos anteriores aplicadas en este periodo. Casillas: [78]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Cuotas a compensar de periodos previos pendientes para periodos posteriores. Casillas: ([110] - [78]) [87]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Exclusivamente para sujetos pasivos que tributan conjuntamente a la Administración del Estado y a las Haciendas Forales Resultado de la regularización anual. Casillas: [68]
        datos += self._convertir_a_centimos_str(resultado_autoliquidacion)  # Resultado - Resultado de la autoliquidación. Casillas: ( [66] + [77] - [78] + [68] ) [69]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Resultados a ingresar de anteriores autoliquidaciones o liquidaciones administrativas correspondientes al ejercicio y período objeto de la autoliquidación. Casillas: [70]
        datos += self._convertir_a_centimos_str(0.0)  # Resultado - Devoluciones acordadas por la Agencia Tributaria como consecuencia de la tramitación de anteriores autoliquidaciones correspondientes al ejercicio y período objeto de la autoliquidación [109]
        datos += self._convertir_a_centimos_str(resultado_final)  # Resultado - Resultado. Casillas: ( [69] - [70] + [109] ) [71]
        datos += "".ljust(1, ' ')  # Declaración Sin actividad (X o blanco)
        datos += "".ljust(1, ' ')  # Declaración complementaria (X o blanco)
        datos += self._RESERVADO_ADMON_13_ESPACIOS  # Número justificante declaración anterior
        datos += self._RESERVADO_ADMON_35_ESPACIOS  # Reservado para la AEAT
        datos += self._RESERVADO_ADMON_86_ESPACIOS  # Reservado para la AEAT
        datos += self._RESERVADO_ADMON_479_ESPACIOS  # Reservado para la AEAT
        datos += self._DP30303_CIERRE  # Indicador de fin de registro página 3
        return datos

    def _generar_dp303_04(self):
        """
        Genera los datos de la seccion DP30304 del modelo 303.
        """

        datos = self._DP30304_APERTURA
        datos += "".ljust(1, ' ')  # Indicador de página complementaria.
        datos += "A01"  # Código de actividad - Principal
        datos += "8612"  # Epígrafe IAE - Principal
        datos += "".ljust(3, ' ')  # Código de actividad - Otras - 1ª
        datos += "".ljust(4, ' ')  # Epígrafe IAE - Otras - 1ª
        datos += "".ljust(3, ' ')  # Código de actividad - Otras - 2ª
        datos += "".ljust(4, ' ')  # Epígrafe IAE - Otras - 2ª
        datos += "".ljust(3, ' ')  # Código de actividad - Otras - 3ª
        datos += "".ljust(4, ' ')  # Epígrafe IAE - Otras - 3ª
        datos += "".ljust(3, ' ')  # Código de actividad - Otras - 4ª
        datos += "".ljust(4, ' ')  # Epígrafe IAE - Otras - 4ª
        datos += "".ljust(3, ' ')  # Código de actividad - Otras - 5ª
        datos += "".ljust(4, ' ')  # Epígrafe IAE - Otras - 5ª
        datos += "".ljust(1, ' ')  # Marque si ha efectuado operaciones por las que tenga obligación de presentar la declaración anual de operaciones con terceras personas. (X o blanco)
        datos += self._porcentaje_str(0.0)  # Información de la tributación por razón de territorio: Álava [89]
        datos += self._porcentaje_str(0.0)  # Información de la tributación por razón de territorio: Guipuzcoa [90]
        datos += self._porcentaje_str(0.0)  # Información de la tributación por razón de territorio: Vizcaya [91]
        datos += self._porcentaje_str(0.0)  # Información de la tributación por razón de territorio: Navarra [92]
        datos += self._porcentaje_str(0.0)  # Información de la tributación por razón de territorio: Territorio común [107]
        datos += self._convertir_a_centimos_str(self.volumen_anual_operaciones)  # Operaciones realizadas en el ejercicio - Operaciones en régimen general [80]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones en régimen especial del criterio de caja conforme art. 75 LIVA [81]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Entregas intracomunitarias de bienes y servicios [93]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Exportaciones y otras operaciones exentas con derecho a deducción [94]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones exentas sin derecho a deducción [83]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones no sujetas por reglas de localización (excepto las incluidas en la casilla 126) [84]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones sujetas con inversión del sujeto pasivo [125]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones no sujetas por reglas de localización acogidas a los regímenes especiales de ventanilla única [126]
        datos += self._convertir_a_centimos_str(0.0)  # OSS. Operaciones sujetas y acogidas a los regímenes especiales de ventanilla única [127]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones intragrupo valoradas conforme a lo dispuesto en los arts. 78 y 79 LIVA [128]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones en régimen simplificado [86]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones en régimen especial de la agricultura, ganadería y pesca [95]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones realizadas por sujetos pasivos acogidos al régimen especial del recargo de equivalencia [96]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones en Régimen especial de bienes usados, objetos de arte, antigüedades y objetos de colección [97]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Operaciones en régimen especial de Agencias de Viajes [98]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Entregas de bienes inmuebles, operaciones financieras y relativas al oro de inversión no habituales [79]
        datos += self._convertir_a_centimos_str(0.0)  # Operaciones realizadas en el ejercicio - Entregas de bienes de inversión [99]
        datos += self._convertir_a_centimos_str(self.volumen_anual_operaciones)  # Operaciones realizadas en el ejercicio - Total volumen de operaciones ([80]+[81]+[93]+[94]+[83]+[84]+[125]+[126]+[127]+[128]+[86]+[95]+[96]+[97]+[98]-[79]-[99]) [88]
        datos += self._RESERVADO_ADMON_600_ESPACIOS  # Reservado para la AEAT
        datos += self._DP30304_CIERRE
        return datos

    def _generar_dp303_05(self):
        """
        Genera los datos de la seccion DP30305 del modelo 303.
        """

        datos = self._DP30305_APERTURA
        datos += "".ljust(1, ' ')  # Indicador de página complementaria.
        datos += "".ljust(3, ' ')  # Prorratas - 1 - Código CNAE [500]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 1 - Importe de operaciones [501]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 1 - Importe de operaciones con derecho a deducción [502]
        datos += "".ljust(1, ' ')  # Prorratas - 1 - Tipo de prorrata ("G", "E" o blanco). [503]
        datos += self._porcentaje_str(0.0)  # Prorratas - 1 - % de prorrata [504]
        datos += "".ljust(3, ' ')  # Prorratas - 2 - Código CNAE [505]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 2 - Importe de operaciones [506]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 2 - Importe de operaciones con derecho a deducción [507]
        datos += "".ljust(1, ' ')  # Prorratas - 2 - Tipo de prorrata ("G", "E" o blanco). [508]
        datos += self._porcentaje_str(0.0)  # Prorratas - 2 - % de prorrata [509]
        datos += "".ljust(3, ' ')  # Prorratas - 3 - Código CNAE [510]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 3 - Importe de operaciones [511]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 3 - Importe de operaciones con derecho a deducción [512]
        datos += "".ljust(1, ' ')  # Prorratas - 3 - Tipo de prorrata ("G", "E" o blanco). [513]
        datos += self._porcentaje_str(0.0)  # Prorratas - 3 - % de prorrata [514]
        datos += "".ljust(3, ' ')  # Prorratas - 4 - Código CNAE [515]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 4 - Importe de operaciones [516]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 4 - Importe de operaciones con derecho a deducción [517]
        datos += "".ljust(1, ' ')  # Prorratas - 4 - Tipo de prorrata ("G", "E" o blanco). [518]
        datos += self._porcentaje_str(0.0)  # Prorratas - 4 - % de prorrata [519]
        datos += "".ljust(3, ' ')  # Prorratas - 5 - Código CNAE [520]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 5 - Importe de operaciones [521]
        datos += self._convertir_a_centimos_str(0.0)  # Prorratas - 5 - Importe de operaciones con derecho a deducción [522]
        datos += "".ljust(1, ' ')  # Prorratas - 5 - Tipo de prorrata ("G", "E" o blanco). [523]
        datos += self._porcentaje_str(0.0)  # Prorratas - 5 - % de prorrata [524]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Operac. Interiores - Bienes y servicios corrientes - Base imponible [700]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Operac. Interiores - Bienes y servicios corrientes - Cuota deducible [701]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Operac. Interiores - Bienes inversión - Base imponible [702]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Operac. Interiores - Bienes inversión - Cuota deducible [703]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Importaciones - Bienes corrientes - Base imponible [704]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Importaciones - Bienes corrientes - Cuota deducible [705]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Importaciones - Bienes inversión - Base imponible [706]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Importaciones - Bienes inversión - Cuota deducible [707]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Adquisic. intracomun. - Bienes corrientes y servicios - Base imponible [708]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Adquisic. intracomun. - Bienes corrientes y servicios - Cuota deducible [709]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Adquisic. intracomun. - Bienes inversión - Base imponible [710]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - IVA ded. Adquisic. intracomun. - Bienes inversión - Cuota deducible [711]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - Compensac. rég. especial agric./ganad./pesca - Base impon. [712]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - Compensac. rég. especial agric./ganad./pesca - Cuota deduc. [713]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - Rectificación de deducciones - Base impon.  [714]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - Rectificación de deducciones - Cuota deduc. [715]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - Regularización de bienes de inversión [716]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 1 - Suma de deducciones [717]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Operac. Interiores - Bienes y servicios corrientes - Base imponible [718]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Operac. Interiores - Bienes y servicios corrientes - Cuota deducible [719]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Operac. Interiores - Bienes inversión - Base imponible [720]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Operac. Interiores - Bienes inversión - Cuota deducible [721]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Importaciones - Bienes corrientes - Base imponible [722]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Importaciones - Bienes corrientes - Cuota deducible [723]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Importaciones - Bienes inversión - Base imponible [724]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Importaciones - Bienes inversión - Cuota deducible [725]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Adquisic. intracomun. - Bienes corrientes y servicios - Base imponible [726]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Adquisic. intracomun. - Bienes corrientes y servicios - Cuota deducible [727]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Adquisic. intracomun. - Bienes inversión - Base imponible [728]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - IVA ded. Adquisic. intracomun. - Bienes inversión - Cuota deducible [729]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - Compensac. rég. especial agric./ganad./pesca - Base impon. [730]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - Compensac. rég. especial agric./ganad./pesca - Cuota deduc. [731]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - Rectificación de deducciones - Base impon.  [732]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - Rectificación de deducciones - Cuota deduc. [733]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - Regularización de bienes de inversión [734]
        datos += self._convertir_a_centimos_str(0.0)  # 13. Reg. Deducc. Diferenc.- 2 - Suma de deducciones [735]
        datos += self._RESERVADO_ADMON_672_ESPACIOS
        datos += self._DP30305_CIERRE
        return datos

    def _generar_dp303_did(self):
        """
        Genera los datos de la seccion DP303DID del modelo 303.
        """

        datos = self._DP303DID_APERTURA
        datos += "".ljust(11, ' ')  # Devolución. SWIFT-BIC
        if (self._calcula_couta() < 0):
            # Si la cuota es negativa no se incluye el IBAN
            datos += "".ljust(34, ' ')  # Domiciliación/Devolución - IBAN
        else:
            # Si la cuota es positiva se incluye el IBAN
            datos += self.iban.ljust(34, ' ')  # Domiciliación/Devolución - IBAN
        datos += "".ljust(70, ' ')  # Devolución - Banco/Bank name
        datos += "".ljust(35, ' ')  # Devolución - Dirección del Banco/ Bank address
        datos += "".ljust(30, ' ')  # Devolución - Ciudad/City
        datos += "".ljust(2, ' ')  # Devolución - Código País/Country code
        datos += self._marca_sepa(self.iban)  # Devolución - Marca SEPA (0 - Vacía, 1 - Cuenta España, 2 - Unión Europea SEPA, 3 - Resto Países)
        datos += self._RESERVADO_ADMON_617_ESPACIOS
        datos += self._DP303DID_CIERRE
        return datos

    def _calcula_couta(self):
        iva_devengado = round(self.base_imponible * 0.21, 2)
        total_iva_deducible = round(self.iva_gastos_bienes_servicios + self.iva_adquisiciones_bienes_inversion, 2)
        return round(iva_devengado - total_iva_deducible, 2)

    def _tipo_declaracion(self):
        """
        Obtiene el tipo de declaración en base al IVA devengado y el IBAN.
        Sólo tiene en cuenta los tipos N, U e I. El resto de tipos no están soportados.
        El tipo de declaración puede ser:
        C (solicitud de compensación)
        D (devolución)
        G (cuenta corriente tributaria-ingreso)
        I (ingreso)
        N (sin actividad/resultado cero)
        V (cuenta corriente tributaria -devolución)
        U (domiciliacion del ingreso en CCC)
        X (Devolución por transferencia al extranjero)
        """
        cuota = self._calcula_couta()

        if (cuota == 0):
            return "N"
        if (cuota < 0 and not self.periodo == "4T"):
            return "C"
        if (cuota < 0 and self.periodo == "4T"):
            return "D"
        if (cuota > 0 and self.iban is not None and self.iban != ""):
            return "U"
        return "I"

    def _exoneracion_modelo_390(self, periodo):
        """
        Obtiene el valor a añadir para la exoneración del Modelo 390 dependiendo del periodo.

        :param periodo: Periodo para el cual se generan los datos.
        :type string: Periodo
        :return: String con valor a añadir para la exoneración del Modelo 390 dependiendo del periodo.
        :rtype: String.
        """
        if (periodo != "4T"):
            return self._NO_ES_4T
        return self._SI

    def _operaciones_distinto_0(self, periodo):
        if (periodo != "4T"):
            return self._NO_ES_4T
        return self._SI

    def _marca_sepa(self, iban):
        return "0"

    def _convertir_a_centimos(self, valor):
        return int(round(valor * 100, 2))

    def _convertir_a_centimos_zfill(self, valor, len):
        resultado = str(self._convertir_a_centimos(abs(valor))).zfill(len)
        if (valor < 0):
            return "N" + resultado[1:]
        else:
            return resultado

    def _convertir_a_centimos_str(self, valor):
        return self._convertir_a_centimos_zfill(valor, 17)

    def _porcentaje_str(self, valor):
        return self._convertir_a_centimos_zfill(valor, 5)

    def _base_cuota_str(self, base, cuota):
        return self._convertir_a_centimos_str(base) + self._convertir_a_centimos_str(cuota)

    def _base_tipo_cuota_str(self, base, tipo, cuota):
        return self._convertir_a_centimos_str(base) + self._porcentaje_str(tipo) + self._convertir_a_centimos_str(cuota)
