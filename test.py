import logging
import logging.config

# Charger la configuration de logging
logging.config.fileConfig('logging.conf')

# Créer un logger
logger = logging.getLogger(__name__)

# Utiliser le logger
logger.debug('Message de debug')
logger.info('Message d\'information')
logger.warning('Message d\'avertissement')
logger.error('Message d\'erreur')
logger.critical('Message critique')
