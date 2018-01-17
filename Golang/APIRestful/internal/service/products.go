package service

import (
  "database/sql"
)

type Product struct {
  ID    int     `json:"id"`
  Name  string  `json:"name"`
  Metadata string `json:"metadata"`
}

func (p *Product) GetProduct(db *sql.DB) error {
    return db.QueryRow("SELECT name, metadata FROM auth.products WHERE id=$1",
        p.ID).Scan(&p.Name, &p.Metadata)
}

func (p *Product) UpdateProduct(db *sql.DB) error {
    _, err :=
        db.Exec("UPDATE auth.products SET name=$1, metadata=$2 WHERE id=$3",
            p.Name, p.Metadata, p.ID)

    return err
}

func (p *Product) DeleteProduct(db *sql.DB) error {
    _, err := db.Exec("DELETE FROM auth.products WHERE id=$1", p.ID)

    return err
}

func (p *Product) CreateProduct(db *sql.DB) error {
    err := db.QueryRow(
        "INSERT INTO auth.products(name, metadata) VALUES($1, $2) RETURNING id",
        p.Name, p.Metadata).Scan(&p.ID)

    if err != nil {
        return err
    }

    return nil
}

func GetProducts(db *sql.DB, start, count int, filterParams map[string][]string) ([]Product, error) {
    queryString := "SELECT id, name, metadata FROM auth.products "
    queryString += getWhereQuery(filterParams)

    rows, err := db.Query(queryString+" LIMIT $1 OFFSET $2", count, start)

    if err != nil {
        return nil, err
    }

    defer rows.Close()

    products := []Product{}

    for rows.Next() {
        var p Product
        if err := rows.Scan(&p.ID, &p.Name, &p.Metadata); err != nil {
            return nil, err
        }
        products = append(products, p)
    }

    return products, nil
}
