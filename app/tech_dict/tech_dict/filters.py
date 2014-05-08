class Filters(object):
    '''
    '''
    def __init__(self, req, sort_default='-created_at'):
        super(Filters, self).__init__()
        self.formater = '%Y-%m-%d'  # '2014-01-01'
        self.time_zone = time_zone
        self.startIndex = self.get_num(req.get('startIndex'), 0)
        self.maxResults = self.get_num(req.get('maxResults'), 10)
        self.start_date = req.get('startDate', None)
        self.end_date = req.get('endDate', None)
        self.filters_str = req.get('filters', None)

        sort = req.get('sort') if req.get('sort', None) else sort_default
        self.reverse = False
        self.sort = sort
        if sort.startswith('-'):
            self.reverse = True
            self.sort = sort[1:]
