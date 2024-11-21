% bola_de_nieve.pl

% Dinámico: para agregar o quitar hechos (tarjetas) en tiempo de ejecución
:- dynamic tarjeta/3.

% Predicado que almacena cada tarjeta con su saldo, pago minimo y el id
% tarjeta(ID, Saldo, PagoMinimo).
tarjeta(1, 1000, 100).
tarjeta(2, 500, 50).
tarjeta(3, 1500, 150).

% Regla para ordenar las tarjetas por saldo (metodo bola de nieve)
orden_bola_de_nieve(Orden) :-
    findall(Saldo-ID-PagoMinimo, tarjeta(ID, Saldo, PagoMinimo), Tarjetas),
    sort(1, @=<, Tarjetas, TarjetasOrdenadas), % Ordena por saldo ascendente
    pairs_values(TarjetasOrdenadas, Orden).

% Regla para calcular el fondo de emergencia y el dinero disponible para deuda
calcular_fondo_disponible(Sueldo, Gastos, FondoEmergencia, DisponibleParaDeuda) :-
    Resta is Sueldo - Gastos, % Resta el sueldo de los gastos básicos
    FondoEmergencia is Resta * 0.25, % 25% para fondo de emergencia
    DisponibleParaDeuda is Resta - FondoEmergencia. % Lo restante es para deudas

% Limpia todas las tarjetas (útil para ejecutar nuevas consultas)
limpiar_tarjetas :-
    retractall(tarjeta(_, _, _)).
