describe("Venda de produtos", function() {
    //expect(foo).toBeTruthy();
    //expect(a).not.toEqual(b);
    //expect(a).toBeFalsy();
    //expect(foo).toEqual(1);

    beforeEach(function() {
        _gaq = []
        if($("#produtos-section").length == 0){
            $("body").append(vendaProdutosFixture);
        }
        this.context = $("#produtos-section");
    });

    afterEach(function() {
    });

    it("Nao deixar comprar camisas", function() {
        expect(_gaq.length).toEqual(0);
        spyOn(window, "alert");
        var submitCallback = jasmine.createSpy().andReturn(false);
        $(".pague-com-pag-seguro form", this.context).submit(submitCallback);
        $(".quantidade-cada-camisa:first", this.context).val('2');
        $(".pague-com-pag-seguro input[type=image]", this.context).click();
        expect(_gaq.length).toEqual(1);
        expect(window.alert).toHaveBeenCalled();
        expect(submitCallback).toHaveBeenCalled();
    });

});


