describe("Venda de produtos", function() {
    //expect(foo).toBeTruthy();
    //expect(a).not.toEqual(b);
    //expect(a).toBeFalsy();
    //expect(foo).toEqual(1);

    beforeEach(function() {
        $("body").append(minhasBandasFixtureHtml);
        main_index();
        this.context = $("#minhas-bandas");

        _gaq = [];

        this.assertClickedBtn = function(elm){
            expect(_gaq.length).toEqual(0);

            runs(function(){
                elm.click();
            });

            waits(500);

            runs(function () {
                expect(_gaq.length).toEqual(1);
            });
        };

        this.assertChangedSelect = function(elm){
            expect(_gaq.length).toEqual(0);

            runs(function(){
                elm.val(2);
                elm.change();
            });

            waits(500);

            runs(function () {
                expect(_gaq.length).toEqual(1);
            });
        };
    });

    afterEach(function() {
        this.context.remove();
    });

    it("Favoritar a banda", function() {
        var elm = $(".favoritar:first");
        runs(function(){
            this.assertClickedBtn(elm);
        });

        waits(500);

        runs(function () {
            expect(_gaq[0][2]).toEqual('Favoritar em uma pesquisa de banda');
            expect(_gaq[0][3]).toEqual('Banda: The Beatles');
            expect(elm.hasClass("favoritou")).toBeTruthy();
        });
    });

    it("Nota da banda", function() {
        var elm = $(".nota:first");
        runs(function(){
            this.assertChangedSelect(elm);
        });

        waits(500);

        runs(function () {
            expect(_gaq[0][2]).toEqual('Nota em uma pesquisa de banda');
            expect(_gaq[0][3]).toEqual('Banda: The Beatles Nota: 2');
        });
    });

});
