require(['gitbook', 'jquery'], function(gitbook, $) {

    const ZIP_BUTTON_ID = 'zip-button';  // ID único para el botón ZIP

    gitbook.events.bind('page.change', function(e, config) {
        gitbook.toolbar.removeButton(ZIP_BUTTON_ID);
        console.log(`Botón ${ZIP_BUTTON_ID} eliminado antes de cargar la nueva página.`);

        var currentPage = window.location.pathname.split('/').pop().replace('.html', '');
        console.log(`Cambiando de página a: ${currentPage}`);

        // Verificar si hay un ZIP asociado en zipData
        if (zipData.hasOwnProperty(currentPage)) {
            var zipUrl = zipData[currentPage];
            console.log(`Archivo ZIP encontrado para ${currentPage}: ${zipUrl}`);

            gitbook.toolbar.createButton({
                id: ZIP_BUTTON_ID,
                icon: 'fa fa-download',
                label: 'Descargar Datos',
                position: 'right',
                onClick: function(e) {
                    e.preventDefault();
                    window.open(zipUrl, '_blank');
                }
            });

            console.log(`Botón ${ZIP_BUTTON_ID} creado.`);
        } else {
            console.log(`No se encontró archivo ZIP para ${currentPage}.`);
        }
    });

});
