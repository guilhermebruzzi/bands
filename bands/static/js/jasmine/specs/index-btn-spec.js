describe("Botoes fake na home", function() {
    //expect(foo).toBeTruthy();
    //expect(a).not.toEqual(b);
    //expect(a).toBeFalsy();
    //expect(foo).toEqual(1);

    beforeEach(function() {
        $("body").append(indexBtnFixture);
        main_index();
        this.context = $(".area-login-botoes");
        _gaq = [];

        this.assertClickedBtn = function(elm){
            expect(_gaq.length).toEqual(0);
            spyOn(window, "alert");

            runs(function(){
                elm.click();
            });

            waits(500);

            runs(function () {
                expect(window.alert).toHaveBeenCalled();
                expect(_gaq.length).toEqual(1);
            });
        };
    });

    afterEach(function() {
        this.context.remove();
    });

    it("Botao Gmail", function() {
        this.assertClickedBtn($("#gmail-btn"));
    });

    it("Botao Bands", function() {
        this.assertClickedBtn($("#conta-bands-btn"));
    });

});


