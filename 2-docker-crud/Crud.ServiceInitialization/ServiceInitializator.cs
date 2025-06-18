using Crud.DAL.Implementations.User;
using Crud.DAL.Interfaces;
using Microsoft.Extensions.DependencyInjection;

namespace Crud.ServiceInitialization
{
    public static class ServiceInitializator
    {
        public static IServiceCollection Initialize(this IServiceCollection services)
        {
            services.AddScoped<IUserDAL, UserDAL>();

            return services;
        }
    }
}