using Crud.DAL.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Crud.DAL.Implementations.User
{
    public class UserDAL : IUserDAL
    {
        private readonly DataContext _dataContext;

        public UserDAL(DataContext dataContext)
        {
            _dataContext = dataContext;
        }

        public async Task DeleteAsync(Model.User user)
        {
            _dataContext.Users.Remove(user);
        }

        public Task<List<Model.User>> GetAllAsync()
        {
            return _dataContext.Users.ToListAsync();
        }

        public Task<Model.User> GetByIdAsync(long id)
        {
            return _dataContext.Users.FirstOrDefaultAsync(u => u.Id == id);
        }

        public async Task InsertAsync(Model.User user)
        {
            await _dataContext.Users.AddAsync(user);
        }

        public async Task UpdateAsync(Model.User user)
        {
            _dataContext.Users.Update(user);
        }
    }
}