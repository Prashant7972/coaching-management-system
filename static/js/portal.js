// Portal Helper Scripts - VidyaSetu Career Institute

document.addEventListener('DOMContentLoaded', function () {
    // Attendance Helper: Mark All as Present
    const markAllPresentBtn = document.getElementById('btn-mark-all-present');
    if (markAllPresentBtn) {
        markAllPresentBtn.addEventListener('click', function () {
            const radioButtons = document.querySelectorAll('input[type="radio"][value="PRESENT"]');
            radioButtons.forEach(radio => {
                radio.checked = true;
            });
        });
    }

    // Attendance Helper: Mark All as Absent
    const markAllAbsentBtn = document.getElementById('btn-mark-all-absent');
    if (markAllAbsentBtn) {
        markAllAbsentBtn.addEventListener('click', function () {
            const radioButtons = document.querySelectorAll('input[type="radio"][value="ABSENT"]');
            radioButtons.forEach(radio => {
                radio.checked = true;
            });
        });
    }

    // Interactive Fee Concession Range Slider Calculator
    const scholarshipSlider = document.getElementById('scholarshipRange');
    const sliderValDisplay = document.getElementById('sliderPercentDisplay');
    const concessionDisplay = document.getElementById('concessionAmountDisplay');
    const netFeeDisplay = document.getElementById('netFeeDisplay');
    const installmentDisplay = document.getElementById('installmentDisplay');
    const courseSelect = document.getElementById('sliderCourseSelect');

    function formatIndianRupee(num) {
        const val = Math.round(num);
        let s = val.toString();
        if (s.length <= 3) return '₹' + s;
        let last3 = s.substring(s.length - 3);
        let other = s.substring(0, s.length - 3);
        let result = '';
        while (other.length > 2) {
            result = ',' + other.substring(other.length - 2) + result;
            other = other.substring(0, other.length - 2);
        }
        if (other.length > 0) {
            result = other + result;
        }
        return '₹' + result + ',' + last3;
    }

    function updateFeeCalculation() {
        if (!scholarshipSlider) return;
        const percent = parseInt(scholarshipSlider.value, 10);
        const baseFee = parseFloat(courseSelect ? courseSelect.value : 148000);
        
        if (sliderValDisplay) sliderValDisplay.textContent = percent + '%';
        
        const concession = (baseFee * percent) / 100;
        const netFee = baseFee - concession;
        const installment = netFee / 2;

        if (concessionDisplay) concessionDisplay.textContent = formatIndianRupee(concession);
        if (netFeeDisplay) netFeeDisplay.textContent = formatIndianRupee(netFee);
        if (installmentDisplay) installmentDisplay.textContent = formatIndianRupee(installment);
    }

    if (scholarshipSlider) {
        scholarshipSlider.addEventListener('input', updateFeeCalculation);
        if (courseSelect) {
            courseSelect.addEventListener('change', updateFeeCalculation);
        }
        // Preset buttons
        document.querySelectorAll('.btn-preset-slider').forEach(btn => {
            btn.addEventListener('click', function () {
                const targetVal = this.getAttribute('data-val');
                scholarshipSlider.value = targetVal;
                updateFeeCalculation();
            });
        });
        updateFeeCalculation();
    }

    // Auto dismiss standard alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                alert.style.display = 'none';
            }
        }, 6000);
    });
});
