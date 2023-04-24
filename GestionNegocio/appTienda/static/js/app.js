function abrirModalEliminar(idProducto){
    Swal.fire({
        title: 'Eliminar Producto',
        text: "¿Esta seguro de eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si',
        cancelButtonText: 'No'
    }).then((result) => {
        if(result.isConfirmed){
            location.href="/eliminarProducto/"+idProducto+"/"
        }
    })
}