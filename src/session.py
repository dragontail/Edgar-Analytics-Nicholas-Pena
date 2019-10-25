class Session:
	def __init__(self, ip, timestamp, cik, accession, extention):
		try:
			self.ip = ip
			self.timestamp = timestamp
			self.cik = cik
			self.accession = accession
			self.extention = extention
		except TypeError:
			return None

	def __str__(self):
		string = "ip: {}, timestamp: {}, cik: {}, accession: {}, extention: {}".format(
				self.ip, self.timestamp, self.cik, self.accession, self.extention
			) 
		return string
