package ar.edu.itba.ss;

public class Config {
    private Double mass;
    private Double k;
    private Double gamma;
    private Double r0;
    private Double v0;
    private Double a0;
    private Double t0;
    private Double dt;
    private String method;
    private Integer steps;

    public Config(Double mass, Double k, Double gamma, Double r0, Double v0, Double a0, Double t0, Double dt,
            String method, Integer steps) {
        this.mass = mass;
        this.k = k;
        this.gamma = gamma;
        this.r0 = r0;
        this.v0 = v0;
        this.a0 = a0;
        this.t0 = t0;
        this.dt = dt;
        this.method = method;
        this.steps = steps;
    }

    public Double getMass() {
        return mass;
    }

    public void setMass(Double mass) {
        this.mass = mass;
    }

    public Double getK() {
        return k;
    }

    public void setK(Double k) {
        this.k = k;
    }

    public Double getGamma() {
        return gamma;
    }

    public void setGamma(Double gamma) {
        this.gamma = gamma;
    }

    public Double getR0() {
        return r0;
    }

    public void setR0(Double r0) {
        this.r0 = r0;
    }

    public Double getV0() {
        return v0;
    }

    public void setV0(Double v0) {
        this.v0 = v0;
    }

    public Double getA0() {
        return a0;
    }

    public void setA0(Double a0) {
        this.a0 = a0;
    }

    public Double getT0() {
        return t0;
    }

    public void setT0(Double t0) {
        this.t0 = t0;
    }

    public Double getDt() {
        return dt;
    }

    public void setDt(Double dt) {
        this.dt = dt;
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    @Override
    public String toString() {
        return "Config [mass=" + mass + ", k=" + k + ", gamma=" + gamma + ", r0=" + r0 + ", v0=" + v0 + ", a0=" + a0
                + ", t0=" + t0 + ", dt=" + dt + ", method=" + method + ", steps=" + steps + "]";

    }

    public Integer getSteps() {
        return steps;
    }

    public void setSteps(Integer steps) {
        this.steps = steps;
    }
}
