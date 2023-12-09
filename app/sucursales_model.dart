

class Sucursal {
  String? distribuidor;
  String? id;
  String? distribuidor_id;
  String? nombre;
  String? direccion;
  String? telefono;
  String? email;
  Map? coordenadas;
  Map? horarioAtencion;
  String? gerente;
  DateTime? created;
  DateTime? lastUpdate;
  List? imagenesDistribuidor;
  String? logo;

  Sucursal({
    this.distribuidor,
    this.distribuidor_id,
    this.id,
    this.nombre,
    this.coordenadas,
    this.direccion,
    this.telefono,
    this.email,
    this.created,
    this.lastUpdate,
    this.horarioAtencion,
    this.gerente,
    this.imagenesDistribuidor,
    this.logo,
  });

  // Método para inicializar desde un mapa JSON
  factory Sucursal.fromJson(Map<String, dynamic> json, id) {
    return Sucursal(
      distribuidor: json['distribuidor'],
      distribuidor_id: json['distribuidor_id'],
      nombre: json['nombre'],
      direccion: json['direccion'],
      id: id,
      telefono: json['telefono'],
      email: json['email'],
      coordenadas: json['coordenadas'],
      horarioAtencion: json['horarioAtencion'],
      gerente: json['gerente'],
      created: DateTime.parse(json['created']),
      lastUpdate: DateTime.parse(json['lastUpdate']),
      imagenesDistribuidor: json['imagenesDistribuidor'],
      logo: json['logo'],
    );
  }

  // Método para convertir el objeto en un mapa JSON
  Map<String, dynamic> toJson() {
    return {
      'distribuidor_id': distribuidor_id,
      'id': id,
      'coordenadas': coordenadas,
      'distribuidor': distribuidor,
      'nombre': nombre,
      'direccion': direccion,
      'lastUpdate': lastUpdate!.toIso8601String(),
      'created': created!.toIso8601String(),
      'telefono': telefono,
      'email': email,
      'horarioAtencion': horarioAtencion,
      'gerente': gerente,
      'imagenesDistribuidor': imagenesDistribuidor,
      'logo': logo,
    };
  }
}
