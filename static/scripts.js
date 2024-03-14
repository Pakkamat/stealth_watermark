document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        // เมื่อหน้าเว็บโหลดเสร็จแล้ว ซ่อน Spinner
        document.getElementById("loader").style.display = "none";
    }
};