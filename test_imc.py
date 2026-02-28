"""Testes de funcionalidade para a Calculadora de IMC."""

import pytest
from imc_app import calcular_imc, classificar_imc, recomendacao_imc


# ── calcular_imc ──────────────────────────────────────────────


class TestCalcularIMC:
    """Testes para o cálculo do IMC."""

    def test_calculo_basico(self):
        """70 kg / 1.75 m => ~22.86"""
        assert round(calcular_imc(70, 1.75), 2) == 22.86

    def test_calculo_peso_alto(self):
        """120 kg / 1.80 m => ~37.04"""
        assert round(calcular_imc(120, 1.80), 2) == 37.04

    def test_calculo_peso_baixo(self):
        """45 kg / 1.70 m => ~15.57"""
        assert round(calcular_imc(45, 1.70), 2) == 15.57

    def test_peso_zero_levanta_erro(self):
        with pytest.raises(ValueError):
            calcular_imc(0, 1.75)

    def test_altura_zero_levanta_erro(self):
        with pytest.raises(ValueError):
            calcular_imc(70, 0)

    def test_valores_negativos_levantam_erro(self):
        with pytest.raises(ValueError):
            calcular_imc(-70, 1.75)
        with pytest.raises(ValueError):
            calcular_imc(70, -1.75)


# ── classificar_imc ──────────────────────────────────────────


class TestClassificarIMC:
    """Testes para a classificação do IMC."""

    def test_baixo_peso(self):
        resultado = classificar_imc(16.0)
        assert resultado["classificacao"] == "Baixo peso"
        assert resultado["cor"] == "🔵"

    def test_peso_normal(self):
        resultado = classificar_imc(22.0)
        assert resultado["classificacao"] == "Peso normal"
        assert resultado["cor"] == "🟢"

    def test_sobrepeso(self):
        resultado = classificar_imc(27.0)
        assert resultado["classificacao"] == "Sobrepeso"
        assert resultado["cor"] == "🟡"

    def test_obesidade(self):
        resultado = classificar_imc(35.0)
        assert resultado["classificacao"] == "Obesidade"
        assert resultado["cor"] == "🔴"

    def test_limite_baixo_peso_normal(self):
        """IMC = 18.5 deve ser Peso normal."""
        assert classificar_imc(18.5)["classificacao"] == "Peso normal"

    def test_limite_normal_sobrepeso(self):
        """IMC = 25.0 deve ser Sobrepeso."""
        assert classificar_imc(25.0)["classificacao"] == "Sobrepeso"

    def test_limite_sobrepeso_obesidade(self):
        """IMC = 30.0 deve ser Obesidade."""
        assert classificar_imc(30.0)["classificacao"] == "Obesidade"

    def test_retorno_contem_chaves_necessarias(self):
        resultado = classificar_imc(22.0)
        assert "classificacao" in resultado
        assert "cor" in resultado
        assert "cor_bg" in resultado


# ── recomendacao_imc ─────────────────────────────────────────


class TestRecomendacaoIMC:
    """Testes para as recomendações baseadas no IMC."""

    def test_recomendacao_baixo_peso(self):
        rec = recomendacao_imc(16.0)
        assert rec["tipo"] == "info"
        assert "nutricionista" in rec["texto"].lower()

    def test_recomendacao_peso_normal(self):
        rec = recomendacao_imc(22.0)
        assert rec["tipo"] == "success"
        assert "parabéns" in rec["texto"].lower()

    def test_recomendacao_sobrepeso(self):
        rec = recomendacao_imc(27.0)
        assert rec["tipo"] == "warning"

    def test_recomendacao_obesidade(self):
        rec = recomendacao_imc(35.0)
        assert rec["tipo"] == "error"
        assert "médico" in rec["texto"].lower()

    def test_retorno_contem_chaves_necessarias(self):
        rec = recomendacao_imc(22.0)
        assert "tipo" in rec
        assert "texto" in rec


# ── Integração: cálculo + classificação ──────────────────────


class TestIntegracao:
    """Testes de integração entre cálculo e classificação."""

    def test_fluxo_completo_peso_normal(self):
        imc = calcular_imc(70, 1.75)
        cls = classificar_imc(imc)
        rec = recomendacao_imc(imc)
        assert cls["classificacao"] == "Peso normal"
        assert rec["tipo"] == "success"

    def test_fluxo_completo_obesidade(self):
        imc = calcular_imc(120, 1.70)
        cls = classificar_imc(imc)
        rec = recomendacao_imc(imc)
        assert cls["classificacao"] == "Obesidade"
        assert rec["tipo"] == "error"

    def test_fluxo_completo_baixo_peso(self):
        imc = calcular_imc(40, 1.80)
        cls = classificar_imc(imc)
        rec = recomendacao_imc(imc)
        assert cls["classificacao"] == "Baixo peso"
        assert rec["tipo"] == "info"

    def test_fluxo_completo_sobrepeso(self):
        imc = calcular_imc(85, 1.75)
        cls = classificar_imc(imc)
        rec = recomendacao_imc(imc)
        assert cls["classificacao"] == "Sobrepeso"
        assert rec["tipo"] == "warning"
