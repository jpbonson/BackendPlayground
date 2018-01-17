package service

func getWhereQuery(filterParams map[string][]string) (string) {
    queryString := ""
    if len(filterParams) != 0 {
        queryString += "WHERE "
        cont := 0
        for k, v := range filterParams {
            queryString += k+"='"+v[0]+"'"
            cont += 1
            if cont < len(filterParams) {
              queryString += " and "
            }
        }
    }
    return queryString
}
