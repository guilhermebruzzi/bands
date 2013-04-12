describe("Venda de produtos", function() {
    //expect(foo).toBeTruthy();
    //expect(a).not.toEqual(b);
    //expect(a).toBeFalsy();
    //expect(foo).toEqual(1);

    beforeEach(function() {
        _gaq = []
        $("body").append(vendaProdutosFixture);
        formPagSeguro = document.querySelector('form[target="pagseguro"]');
        mainVendaProdutos();
        this.context = $("#produtos-section");
    });

    afterEach(function() {
        $("#produtos-section").remove();
    });

    it("Nao deixar comprar camisas", function() {
        expect(_gaq.length).toEqual(0);
        spyOn(window, "alert");
        var submitCallback = jasmine.createSpy().andReturn(false);
        $(".pague-com-pag-seguro form", this.context).submit(submitCallback);
        $(".quantidade-cada-camisa:first", this.context).val('2');
        runs(function(){
            $(".pague-com-pag-seguro form input[type=image]").click();
        });

        waits(500);

        runs(function () {
            expect(_gaq.length).toEqual(1);
            expect(window.alert).toHaveBeenCalled();
            expect(submitCallback).toHaveBeenCalled();
        });


    });

});


