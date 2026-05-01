package com.calculate.insurance.insurancecalculator.controller;

import java.util.LinkedHashMap;
import java.util.Map;

import com.calculate.insurance.insurancecalculator.model.PremiumRequest;
import com.calculate.insurance.insurancecalculator.model.PremiumResponse;
import org.jspecify.annotations.NonNull;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class InsuranceController {

    @PostMapping("/calculate-premium")
    public PremiumResponse calculatePremium(@RequestBody PremiumRequest request) {
        double premium = 0;

        if ("health".equals(request.getInsuranceType())) {
            premium = request.getCoverage() * 0.02 + request.getMembers() * 1000;

            if (request.getAge() > 45) {
                premium = premium + 2000;
            }
        }

        if ("vehicle".equals(request.getInsuranceType())) {
            if ("car".equals(request.getVehicleType())) {
                premium = request.getVehicleValue() * 0.03;
            } else {
                premium = request.getVehicleValue() * 0.02;
            }

            premium = premium + request.getVehicleAge() * 500;
        }

        if ("life".equals(request.getInsuranceType())) {
            premium = request.getCoverage() * 0.015 + request.getTerm() * 300;

            if (request.getAge() > 40) {
                premium = premium + 1500;
            }
        }

        if ("travel".equals(request.getInsuranceType())) {
            premium = request.getTripCost() * 0.01 + request.getDays() * 50 + request.getTravellers() * 300;
        }

        PremiumResponse response = getPremiumResponse(request, premium);

        return response;
    }

    private static @NonNull PremiumResponse getPremiumResponse(PremiumRequest request, double premium) {
        double gst = premium * 0.18;
        double totalAmount = premium + gst;

        Map<Integer, Double> emiOptions = new LinkedHashMap<>();
        emiOptions.put(3, totalAmount / 3);
        emiOptions.put(6, totalAmount / 6);
        emiOptions.put(9, totalAmount / 9);
        emiOptions.put(12, totalAmount / 12);

        PremiumResponse response = new PremiumResponse();
        response.setInsuranceType(request.getInsuranceType());
        response.setPremium(premium);
        response.setGst(gst);
        response.setTotalAmount(totalAmount);
        response.setEmiOptions(emiOptions);
        return response;
    }
}
