// User Lookup Service
function getUserEmail(user) {
  if (!user || !user.profile) return '';
  return user.profile.email;
}
module.exports = { getUserEmail };
