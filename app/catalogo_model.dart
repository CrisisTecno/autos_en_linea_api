

class Catalogo {

  String? id;  
  
  // Sucursal
  String? sucursal;
  String? sucursal_id;

  //auto O ARTICULO
  String? marca;
  String? modelo;
  String? categoria;
  String? ano;
  double? precio;
  String? kilometraje;
  DateTime? created;
  DateTime? lastUpdate;
  //agregar raiting ******

  //agregar::
  DateTime? lastInventoryUpdate;

  //disponibilidad
  bool? enable;
  Map? especificaciones;
  
  String? mainImage;
  String? descripcion;
  String? color;

  //array de string con links
  List? images;

  Catalogo(
      {this.id,
      this.ano,
      this.categoria,
      this.color,
      this.descripcion,
      this.mainImage,
      this.especificaciones,
      this.images,
      this.kilometraje,
      this.created,
      this.enable,
      this.lastInventoryUpdate,
      this.lastUpdate,
      this.marca,
      this.modelo,
      this.precio,
      this.sucursal,
      this.sucursal_id});

  factory Catalogo.fromJson(json, id) {
    return Catalogo(
        id: id,
        ano: json['ano'],
        created: DateTime.parse(json['created']),
        lastInventoryUpdate: DateTime.parse(json['lastInventoryUpdate']),
        lastUpdate: DateTime.parse(json['lastUpdate']),
        enable: json['enable'],
        categoria: json['categoria'],
        color: json['color'],
        descripcion: json['descripcion'],
        especificaciones: json['especificaciones'] ?? {},
        images: json['images'] ?? [],
        kilometraje: json['kilometraje'],
        marca: json['marca'],
        modelo: json['modelo'],
        precio: json['precio'],
        mainImage: json['mainImage'],
        sucursal: json['sucursal'],
        sucursal_id: json['sucursal_id']);
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'ano': ano,
      'categoria': categoria,
      'color': color,
      'descripcion': descripcion,
      'especificaciones': especificaciones,
      'images': images,
      'kilometraje': kilometraje,
      'lastUpdate': lastUpdate!.toIso8601String(),
      'lastInventoryUpdate': lastInventoryUpdate!.toIso8601String(),
      'created': created!.toIso8601String(),
      'enable': enable,
      'mainImage': mainImage,
      'marca': marca,
      'modelo': modelo,
      'precio': precio,
      'sucursal': sucursal,
      'sucursal_id': sucursal_id
    };
  }
}
