var vComposer = (function(vComposer){

    var ComposerRow = function(rowElememt){

        var items = $('.cell');
        
        Object.defineProperties(this,{
            __el: {
                value: element
            },
            __tools: {
                value: $('<div class="composerRowControls"/>') 
            },
            toolItems: {
                value: $('<div class="composerRowControls"/>') 
            },
            toolItems: {
                value: {
                    'move': $('<a href="#"/>'),
                    'layoutControl': $('<div/>'),
                    'edit': $('<a href="#"/>'),
                    'clone': $('<a href="#"/>'),
                    'delete': $('<a href="#"/>')
                },
                enumerable: true
            }
            __grids: {
                value: $('<div class="composerGrids"/>') 
            },
            gridItems: {
                value : createComposerGrid(items),
                enumerable: true
            }
        });
    };

    var createComposerRows = function(itemElements){

        var items = [];

        $.each(itemElements, function(index, val) {
            var item = new ComposerRow(val);

            items.push(item);
        });

        return items;
    }
      
    var Composer = function(element){

        var items = $('.composerRow');

        Object.defineProperties(this,{
            __el: {
                value : element
            },
            items: {
                value : createComposerRows(items),
                enumerable: true
            }
        });
    };

    Object.defineProperties(Composer.prototype,{
        add: {
            value: function(){
                var element = $('<div/>');
                element.addClass('composerRow');

            },
            enumerable: true
        },
        remove: {
            value: function(index){

                var self = this;
                var len = self.items.length;

                if (index > len || index < 0) {
                    throw new Error("Index is out of range");
                }

                var item = this.items[index];
                this.items.splice(index, 1);

                item.__el.remove();

                item = null;

            },
            enumerable: true
        }
    });

    vComposer.createComposer = function(elementId){

        var element = $(elementId);

        if(element.length == 0){
            element = $('<div/>');
            element.attr('id', elementId);
        }
        element.addClass('vComposer');

        return new Composer(element);

    };

    return vComposer;

}(vComposer || {}));
