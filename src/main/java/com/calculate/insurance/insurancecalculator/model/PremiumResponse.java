package com.calculate.insurance.insurancecalculator.model;

import java.util.Map;

public class PremiumResponse {

    private String insuranceType;
    private double premium;
    private double gst;
    private double totalAmount;
    private Map<Integer, Double> emiOptions;

    public String getInsuranceType() {
        return insuranceType;
    }

    public void setInsuranceType(String insuranceType) {
        this.insuranceType = insuranceType;
    }

    public double getPremium() {
        return premium;
    }

    public void setPremium(double premium) {
        this.premium = premium;
    }

    public double getGst() {
        return gst;
    }

    public void setGst(double gst) {
        this.gst = gst;
    }

    public double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(double totalAmount) {
        this.totalAmount = totalAmount;
    }

    public Map<Integer, Double> getEmiOptions() {
        return emiOptions;
    }

    public void setEmiOptions(Map<Integer, Double> emiOptions) {
        this.emiOptions = emiOptions;
    }
}
