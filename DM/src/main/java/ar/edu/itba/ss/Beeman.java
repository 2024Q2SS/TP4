package ar.edu.itba.ss;

public class Beeman extends Oscillator {

    private Double aPrev;

    public Beeman(Double m, Double k, Double gamma, Double r, Double v, Double a, Double t, Double dt) {
        super(m, k, gamma, r, v, a, t, dt);
    }

    @Override
    public Oscillator create() {
        return new Beeman(getM(), getK(), getGamma(), getR(), getV(), getA(), getT(), getDt());
    }

    @Override
    public void coupledStep(Double prevY, Double nextY) {
        // Primero, calculamos la aceleración actual usando las posiciones previas a la
        // actualización
        double aCurrent = (-getK() * (getR() - prevY) - getK() * (getR() - nextY)) / getM();

        // Cálculo de la nueva posición en y utilizando Beeman
        double yNext = getR() + getV() * getDt() + 2.0 / 3.0 * aCurrent * getDt() * getDt()
                - 1.0 / 6.0 * aPrev * getDt() * getDt();

        // Cálculo de la nueva aceleración acoplada usando la nueva posición y las
        // posiciones prevY y nextY
        double aNext = (-getK() * (yNext - prevY) - getK() * (yNext - nextY)) / getM();

        // Predicción de la nueva velocidad en y usando Beeman
        double vNext = getV() + 1.0 / 3.0 * aNext * getDt() + 5.0 / 6.0 * aCurrent * getDt()
                - 1.0 / 6.0 * aPrev * getDt();

        // Actualizamos los valores previos de aceleración para el próximo paso
        aPrev = aCurrent;

        // Actualizamos las variables
        setR(yNext); // Nueva posición
        setV(vNext); // Nueva velocidad
        setA(aNext); // Nueva aceleración

        // Incrementamos el tiempo de la simulación
        this.setT(this.getT() + this.getDt());
    }

    @Override
    public void firstStep(Double A, Double omega) {
        setR(A * Math.sin(omega * getT()));
        this.setT(this.getT() + this.getDt());
    }

    @Override
    public void lastStep() {
        this.setT(this.getT() + this.getDt());
        return;
    }

    public void initializeValues() {
        double vPrev = getV() + getDt() * getA();
        double rPrev = getR() + getDt() * vPrev + getDt() * getDt() * getA() / 2;
        aPrev = (-getK() * rPrev - getGamma() * vPrev) / getM();
    }

    public void step() {
        double rNext = getR() + getV() * getDt() + 2.0 / 3.0 * getA() * getDt() * getDt()
                - 1.0 / 6.0 * aPrev * getDt() * getDt();

        double vNext = getV() + 3.0 / 2.0 * getA() * getDt() - 1.0 / 2.0 * aPrev * getDt();
        double aNext = (-getK() * rNext - getGamma() * vNext) / getM();

        vNext = getV() + 1.0 / 3.0 * aNext * getDt() + 5.0 / 6.0 * getA() * getDt() - 1.0 / 6.0 * aPrev * getDt();

        aPrev = getA();

        setR(rNext);
        setV(vNext);
        setA(aNext);
        this.setT(this.getT() + this.getDt());
    }
}
