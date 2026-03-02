{
    'name': 'Source Document Link Navigator',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Convierte la referencia de origen en un hipervínculo clickeable hacia el documento fuente',
    'description': """
        Este módulo convierte el campo "Source Document" / "Origen" en un enlace
        clickeable en los siguientes documentos:
        - Órdenes de Compra (Purchase Order) → enlace a la Orden de Venta origen
        - Transferencias/Entregas (Stock Picking) → enlace al documento origen (SO/PO)
        - Facturas (Account Move) → enlace al documento origen
    """,
    'author': 'Alphaqueb Consulting',
    'website': 'https://www.alphaqueb.com',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'purchase',
        'stock',
        'account',
        'sale_stock',
        'purchase_stock',
    ],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
